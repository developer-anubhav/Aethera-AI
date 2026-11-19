import time
import logging
import uuid
import json
from typing import AsyncGenerator, List, Dict, Optional
from sqlalchemy.orm import Session

from app.repositories.compound_repository import CompoundRepository
from app.ai.factory import get_llm_client
from app.ai.system_prompt import AERA_SYSTEM_PROMPT
from app.ai.context_builder import build_compounds_context
from app.ai.prompt_builder import build_aera_prompt
from app.ai.response_formatter import sanitize_response
from app.ai.citation_service import audit_citations

logger = logging.getLogger("aethera.aera_service")

class AeraService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = CompoundRepository(db)
        self.client = get_llm_client()

    async def chat_stream(
        self,
        compound_slug: str,
        question: str,
        history: List[Dict[str, str]],
        level: str = "university",
        mode: str = "explain",
        compare_with_slug: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        Orchestrate context-aware generation, stream results as Server-Sent Events (SSE),
        and yield performance metadata upon completion.
        """
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        try:
            # 1. Retrieve target compound context
            compound_a = self.repository.get_by_id_or_slug(compound_slug)
            if not compound_a:
                yield f"data: {json.dumps({'type': 'error', 'message': f'Compound context {compound_slug} is not registered in the index database.'})}\n\n"
                return
                
            # 2. Retrieve comparison target (if comparison mode active)
            compound_b = None
            if mode == "compare" and compare_with_slug:
                compound_b = self.repository.get_by_id_or_slug(compare_with_slug)
                if not compound_b:
                    yield f"data: {json.dumps({'type': 'error', 'message': f'Comparison target compound {compare_with_slug} is not registered.'})}\n\n"
                    return

            # 3. Build compound properties context
            retrieval_start = time.time()
            context = build_compounds_context(compound_a, compound_b)
            retrieval_time_ms = int((time.time() - retrieval_start) * 1000)

            # 4. Build prompt
            prompt = build_aera_prompt(
                mode=mode,
                level=level,
                question=question,
                context=context,
                history=history,
                compound_name=compound_a.name,
                compound_formula=compound_a.formula,
                compare_name=compound_b.name if compound_b else "",
                compare_formula=compound_b.formula if compound_b else ""
            )
            
            # Approximate metrics
            prompt_tokens = len(prompt) // 4
            
            logger.info(
                f"[Aera Request {request_id}] Started. Mode={mode}, Level={level}, "
                f"Retrieval={retrieval_time_ms}ms, ApproxPromptTokens={prompt_tokens}"
            )

            full_response = ""
            generation_start = time.time()

            # 5. Connect and stream from Gemini SDK
            async for chunk in self.client.stream_response(prompt, AERA_SYSTEM_PROMPT):
                if chunk:
                    clean_chunk = sanitize_response(chunk)
                    full_response += chunk
                    yield f"data: {json.dumps({'type': 'content', 'delta': clean_chunk})}\n\n"

            generation_time_ms = int((time.time() - generation_start) * 1000)
            total_time_ms = int((time.time() - start_time) * 1000)
            
            # 6. Audit citations in the final text
            allowed_references = list(compound_a.references)
            if compound_b:
                allowed_references.extend(compound_b.references)

            # Audit DOIs and citations
            _, audited_citations = audit_citations(full_response, allowed_references)
            completion_tokens = len(full_response) // 4

            logger.info(
                f"[Aera Response {request_id}] Finished. Generation={generation_time_ms}ms, "
                f"Total={total_time_ms}ms, ApproxCompletionTokens={completion_tokens}"
            )

            # 7. Yield final metadata block
            metadata = {
                "type": "metadata",
                "request_id": request_id,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "retrieval_time_ms": retrieval_time_ms,
                "generation_time_ms": generation_time_ms,
                "total_time_ms": total_time_ms,
                "citations": audited_citations
            }
            yield f"data: {json.dumps(metadata)}\n\n"

        except Exception as e:
            logger.error(f"[Aera Request {request_id}] Execution error: {e}")
            error_msg = str(e)
            if "invalid gemini api key" in error_msg.lower():
                display_msg = "Invalid Gemini API key. Please check the key in backend/.env copied from Google AI Studio."
            else:
                display_msg = f"Aera AI request failed: {error_msg}"
            yield f"data: {json.dumps({'type': 'error', 'message': display_msg})}\n\n"
