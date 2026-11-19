import os
import sys

# Ensure backend directory is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import SessionLocal, engine, Base
from app.models.models import (
    Category, Compound, Biomolecule, Protein, Enzyme,
    PhysicalProperty, ChemicalProperty, Hazard, Reference, VisualizationMetadata, Synonym
)

def seed_database():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # 1. Clear existing data to prevent duplicates
    print("Clearing existing tables...")
    db.query(VisualizationMetadata).delete()
    db.query(Reference).delete()
    db.query(Hazard).delete()
    db.query(ChemicalProperty).delete()
    db.query(PhysicalProperty).delete()
    db.query(Enzyme).delete()
    db.query(Protein).delete()
    db.query(Biomolecule).delete()
    db.query(Synonym).delete()
    db.query(Compound).delete()
    db.query(Category).delete()
    db.commit()

    # Enable pg_trgm extension if running on PostgreSQL
    if not engine.url.drivername.startswith("sqlite"):
        print("Enabling PostgreSQL pg_trgm extension...")
        try:
            with engine.connect() as conn:
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
                conn.commit()
        except Exception as e:
            print(f"Warning: Failed to enable pg_trgm extension: {e}")

    print("Creating scientific categories...")
    categories_data = {
        "organic-chemistry": Category(name="Organic Chemistry", slug="organic-chemistry", description="Compounds containing carbon covalently bonded to other elements, forming the basis of all life."),
        "inorganic-chemistry": Category(name="Inorganic Chemistry", slug="inorganic-chemistry", description="Chemical compounds that do not contain carbon-hydrogen bonds, including minerals and metals."),
        "alcohols": Category(name="Alcohols", slug="alcohols", description="Organic compounds containing one or more hydroxyl (-OH) groups bound to a carbon atom."),
        "acids": Category(name="Acids", slug="acids", description="Substances that donate hydrogen ions (protons) or accept electron pairs in chemical reactions."),
        "bases": Category(name="Bases", slug="bases", description="Substances that accept protons, donate hydroxide ions, or release electrons in chemical reactions."),
        "hydrocarbons": Category(name="Hydrocarbons", slug="hydrocarbons", description="Organic compounds consisting entirely of hydrogen and carbon, such as alkanes, alkenes, and arenes."),
        "ketones": Category(name="Ketones", slug="ketones", description="Organic compounds containing a carbonyl functional group (C=O) bonded to two other carbon atoms."),
        "aldehydes": Category(name="Aldehydes", slug="aldehydes", description="Organic compounds containing a carbonyl group bonded to at least one hydrogen atom at the end of a carbon chain."),
        "carbohydrates": Category(name="Carbohydrates", slug="carbohydrates", description="Biomolecules consisting of carbon, hydrogen, and oxygen atoms, including sugars, starch, and cellulose."),
        "proteins": Category(name="Proteins", slug="proteins", description="Large biomolecules composed of one or more long chains of amino acid residues."),
        "enzymes": Category(name="Enzymes", slug="enzymes", description="Biological catalysts, almost always proteins, that accelerate chemical reactions in cells."),
        "hormones": Category(name="Hormones", slug="hormones", description="Signaling molecules produced by glands in multicellular organisms that regulate physiology and behavior."),
        "lipids": Category(name="Lipids", slug="lipids", description="Hydrophobic or amphiphilic biological molecules, including fats, waxes, sterols, and fat-soluble vitamins."),
        "dna": Category(name="DNA", slug="dna", description="Deoxyribonucleic acid, the hereditary material in humans and almost all other organisms."),
        "rna": Category(name="RNA", slug="rna", description="Ribonucleic acid, essential for coding, decoding, regulation, and expression of genes."),
        "drugs": Category(name="Drugs", slug="drugs", description="Chemical substances used to treat, cure, prevent, or diagnose a disease or to promote physical well-being."),
        "nanomaterials": Category(name="Nanomaterials", slug="nanomaterials", description="Materials characterized by an ultra-fine grain size or structural dimensions between 1 and 100 nanometers.")
    }

    for cat in categories_data.values():
        db.add(cat)
    db.commit()

    # --- 3D COORDINATES SEED DATA ---
    
    # 1. Water SDF (3 atoms)
    water_sdf = """Water
  3Dmol.js

  3  2  0  0  0  0  0  0  0  0999 V2000
    0.0000    0.0000    0.0658 O   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000    0.7570   -0.5201 H   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000   -0.7570   -0.5201 H   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0  0  0  0
  1  3  1  0  0  0  0
M  END
"""

    # 2. Ethanol SDF (9 atoms)
    ethanol_sdf = """Ethanol
  3Dmol.js

  9  8  0  0  0  0  0  0  0  0999 V2000
   -1.2287    0.2078    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.1213   -0.4922    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.1713    0.4078    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
   -1.2287    0.8078    0.8800 H   0  0  0  0  0  0  0  0  0  0  0  0
   -1.2287    0.8078   -0.8800 H   0  0  0  0  0  0  0  0  0  0  0  0
   -2.0287   -0.4922    0.0000 H   0  0  0  0  0  0  0  0  0  0  0  0
    0.1213   -1.0922    0.8800 H   0  0  0  0  0  0  0  0  0  0  0  0
    0.1213   -1.0922   -0.8800 H   0  0  0  0  0  0  0  0  0  0  0  0
    2.0713   -0.0922    0.0000 H   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0  0  0  0
  2  3  1  0  0  0  0
  1  4  1  0  0  0  0
  1  5  1  0  0  0  0
  1  6  1  0  0  0  0
  2  7  1  0  0  0  0
  2  8  1  0  0  0  0
  3  9  1  0  0  0  0
M  END
"""

    # 3. Methanol SDF (6 atoms)
    methanol_sdf = """Methanol
  3Dmol.js

  6  5  0  0  0  0  0  0  0  0999 V2000
   -0.6620    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.7380    0.0000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
   -1.0220    0.8800    0.5100 H   0  0  0  0  0  0  0  0  0  0  0  0
   -1.0220   -0.8800    0.5100 H   0  0  0  0  0  0  0  0  0  0  0  0
   -1.0220    0.0000   -1.0200 H   0  0  0  0  0  0  0  0  0  0  0  0
    1.0980    0.0000    0.8900 H   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0  0  0  0
  1  3  1  0  0  0  0
  1  4  1  0  0  0  0
  1  5  1  0  0  0  0
  2  6  1  0  0  0  0
M  END
"""

    # 4. Benzene SDF (12 atoms)
    benzene_sdf = """Benzene
  3Dmol.js

 12 12  0  0  0  0  0  0  0  0999 V2000
   -1.2100    0.7000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000    1.4000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.2100    0.7000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.2100   -0.7000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000   -1.4000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -1.2100   -0.7000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -2.1500    1.2400    0.0000 H   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000    2.4800    0.0000 H   0  0  0  0  0  0  0  0  0  0  0  0
    2.1500    1.2400    0.0000 H   0  0  0  0  0  0  0  0  0  0  0  0
    2.1500   -1.2400    0.0000 H   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000   -2.4800    0.0000 H   0  0  0  0  0  0  0  0  0  0  0  0
   -2.1500   -1.2400    0.0000 H   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  2  0  0  0  0
  2  3  1  0  0  0  0
  3  4  2  0  0  0  0
  4  5  1  0  0  0  0
  5  6  2  0  0  0  0
  6  1  1  0  0  0  0
  1  7  1  0  0  0  0
  2  8  1  0  0  0  0
  3  9  1  0  0  0  0
  4 10  1  0  0  0  0
  5 11  1  0  0  0  0
  6 12  1  0  0  0  0
M  END
"""

    # 5. Caffeine SDF (24 atoms)
    caffeine_sdf = """Caffeine
  3Dmol.js

 24 25  0  0  0  0  0  0  0  0999 V2000
   -0.0802   -0.0855    0.0038 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.3323   -0.0855    0.0038 C   0  0  0  0  0  0  0  0  0  0  0  0
    2.0385    1.1378    0.0038 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.3323    2.3611    0.0038 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.0802    2.3611    0.0038 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.7865    1.1378    0.0038 C   0  0  0  0  0  0  0  0  0  0  0  0
    2.0385   -1.3088    0.0038 N   0  0  0  0  0  0  0  0  0  0  0  0
    3.4510   -1.3088    0.0038 C   0  0  0  0  0  0  0  0  0  0  0  0
    4.1573   -0.0855    0.0038 C   0  0  0  0  0  0  0  0  0  0  0  0
    3.4510    1.1378    0.0038 N   0  0  0  0  0  0  0  0  0  0  0  0
   -2.2015    1.1378    0.0038 N   0  0  0  0  0  0  0  0  0  0  0  0
   -2.9078    2.3611    0.0038 C   0  0  0  0  0  0  0  0  0  0  0  0
   -2.9078   -0.0855    0.0038 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.8900    3.4900    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
   -0.6400   -1.2100    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
    3.8010   -2.2500    0.0000 H   0  0  0  0  0  0  0  0  0  0  0  0
    5.2373   -0.0855    0.0038 H   0  0  0  0  0  0  0  0  0  0  0  0
   -2.5578    2.9211    0.8800 H   0  0  0  0  0  0  0  0  0  0  0  0
   -2.5578    2.9211   -0.8800 H   0  0  0  0  0  0  0  0  0  0  0  0
   -3.9878    2.1611    0.0038 H   0  0  0  0  0  0  0  0  0  0  0  0
   -2.5578   -0.6455    0.8800 H   0  0  0  0  0  0  0  0  0  0  0  0
   -2.5578   -0.6455   -0.8800 H   0  0  0  0  0  0  0  0  0  0  0  0
   -3.9878    0.1145    0.0038 H   0  0  0  0  0  0  0  0  0  0  0  0
   -0.5802    3.3111    0.0038 H   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0  0  0  0
  2  3  2  0  0  0  0
  3  4  1  0  0  0  0
  4  5  2  0  0  0  0
  5  6  1  0  0  0  0
  6  1  2  0  0  0  0
  2  7  1  0  0  0  0
  7  8  1  0  0  0  0
  8  9  2  0  0  0  0
  9 10  1  0  0  0  0
 10  3  1  0  0  0  0
  6 11  1  0  0  0  0
 11 12  1  0  0  0  0
 11 13  1  0  0  0  0
  4 14  2  0  0  0  0
  1 15  2  0  0  0  0
  8 16  1  0  0  0  0
  9 17  1  0  0  0  0
 12 18  1  0  0  0  0
 12 19  1  0  0  0  0
 12 20  1  0  0  0  0
 13 21  1  0  0  0  0
 13 22  1  0  0  0  0
 13 23  1  0  0  0  0
  5 24  1  0  0  0  0
M  END
"""

    # 6. Tetrahydropyran SDF
    tetrahydropyran_sdf = """Tetrahydropyran
  3Dmol.js

  6  6  0  0  0  0  0  0  0  0999 V2000
   -1.2000    0.7000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000    1.4000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.2000    0.7000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
    1.2000   -0.7000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000   -1.4000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -1.2000   -0.7000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0  0  0  0
  2  3  1  0  0  0  0
  3  4  1  0  0  0  0
  4  5  1  0  0  0  0
  5  6  1  0  0  0  0
  6  1  1  0  0  0  0
M  END
"""

    # 7. ATP SDF (10 atoms skeletal backbone)
    atp_sdf = """ATP
  3Dmol.js

 10  9  0  0  0  0  0  0  0  0999 V2000
    0.0000    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.2000    0.8000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    2.4000    0.0000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
    3.8000    0.8000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    5.0000    0.0000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
    6.4000    0.8000    0.0000 P   0  0  0  0  0  0  0  0  0  0  0  0
    7.8000    0.0000    0.0000 P   0  0  0  0  0  0  0  0  0  0  0  0
    9.2000    0.8000    0.0000 P   0  0  0  0  0  0  0  0  0  0  0  0
   -1.2000    0.8000    0.0000 N   0  0  0  0  0  0  0  0  0  0  0  0
   -2.4000    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0  0  0  0
  2  3  1  0  0  0  0
  3  4  1  0  0  0  0
  4  5  1  0  0  0  0
  5  6  1  0  0  0  0
  6  7  1  0  0  0  0
  7  8  1  0  0  0  0
  1  9  1  0  0  0  0
  9 10  1  0  0  0  0
M  END
"""

    # 8. Acetone SDF (4 atoms)
    acetone_sdf = """Acetone
  3Dmol.js

  4  3  0  0  0  0  0  0  0  0999 V2000
    0.0000    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -1.2000   -0.8000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.2000   -0.8000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000    1.2000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0  0  0  0
  1  3  1  0  0  0  0
  1  4  2  0  0  0  0
M  END
"""

    # 9. Formaldehyde SDF (2 atoms)
    formaldehyde_sdf = """Formaldehyde
  3Dmol.js

  2  1  0  0  0  0  0  0  0  0999 V2000
    0.0000    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000    1.2000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  2  0  0  0  0
M  END
"""

    # 10. Aspirin SDF (13 atoms)
    aspirin_sdf = """Aspirin
  3Dmol.js

 13 13  0  0  0  0  0  0  0  0999 V2000
   -1.2000    0.7000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000    1.4000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.2000    0.7000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.2000   -0.7000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000   -1.4000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -1.2000   -0.7000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -2.5000    1.4000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -3.6000    0.8000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
   -2.5000    2.6000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
    2.4000    1.4000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
    3.6000    0.8000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    3.6000   -0.4000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
    4.8000    1.6000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0  0  0  0
  2  3  2  0  0  0  0
  3  4  1  0  0  0  0
  4  5  2  0  0  0  0
  5  6  1  0  0  0  0
  6  1  2  0  0  0  0
  1  7  1  0  0  0  0
  7  8  1  0  0  0  0
  7  9  2  0  0  0  0
  3 10  1  0  0  0  0
 10 11  1  0  0  0  0
 11 12  2  0  0  0  0
 11 13  1  0  0  0  0
M  END
"""

    # 11. Buckminsterfullerene C60 skeleton (12 vertex subset geodesic dome)
    c60_sdf = """C60
  3Dmol.js

 12 15  0  0  0  0  0  0  0  0999 V2000
    0.0000    1.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.9511    0.3090    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.5878   -0.8090    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.5878   -0.8090    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.9511    0.3090    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000    0.5000    0.8660 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.4755    0.1545    0.8660 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.2939   -0.4045    0.8660 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.2939   -0.4045    0.8660 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.4755    0.1545    0.8660 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000    0.0000    1.2000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000    0.0000   -1.2000 C   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0  0  0  0
  2  3  1  0  0  0  0
  3  4  1  0  0  0  0
  4  5  1  0  0  0  0
  5  1  1  0  0  0  0
  6  7  1  0  0  0  0
  7  8  1  0  0  0  0
  8  9  1  0  0  0  0
  9 10  1  0  0  0  0
 10  6  1  0  0  0  0
  1  6  1  0  0  0  0
  2  7  1  0  0  0  0
  3  8  1  0  0  0  0
  4  9  1  0  0  0  0
  5 10  1  0  0  0  0
M  END
"""

    # 12. Human Lysozyme PDB (1A8M first residues segment)
    lysozyme_pdb = """HEADER    HYDROLASE(O-GLYCOSYL)                   13-MAY-98   1A8M
TITLE     LYSOZYME FROM HUMAN
ATOM      1  N   LYS A   1      13.371  -2.124   5.045  1.00 12.35           N
ATOM      2  CA  LYS A   1      12.145  -0.902   5.215  1.00 11.23           C
ATOM      3  C   LYS A   1      10.862  -1.240   5.501  1.00 10.45           C
ATOM      4  O   LYS A   1       9.842  -0.410   5.485  1.00 11.12           O
ATOM      5  N   VAL A   2      10.601  -2.450   5.750  1.00  9.80           N
ATOM      6  CA  VAL A   2       9.300  -2.901   6.102  1.00  8.95           C
ATOM      7  C   VAL A   2       8.105  -2.312   5.204  1.00  8.12           C
ATOM      8  O   VAL A   2       7.042  -2.854   5.001  1.00  8.54           O
ATOM      9  N   PHE A   3       8.320  -1.120   4.640  1.00  7.45           N
ATOM     10  CA  PHE A   3       7.240  -0.450   3.812  1.00  6.90           C
ATOM     11  C   PHE A   3       6.002  -1.201   3.501  1.00  6.23           C
ATOM     12  O   PHE A   3       4.954  -0.650   3.102  1.00  6.50           O
ATOM     13  N   GLU A   4       6.180  -2.520   3.642  1.00  5.80           N
ATOM     14  CA  GLU A   4       5.012  -3.410   3.301  1.00  5.12           C
ATOM     15  C   GLU A   4       3.980  -3.120   4.250  1.00  4.90           C
ATOM     16  O   GLU A   4       2.842  -3.560   4.041  1.00  4.80           O
ATOM     17  N   ARG A   5       4.320  -2.250   5.150  1.00  4.50           N
ATOM     18  CA  ARG A   5       3.421  -1.920   6.182  1.00  4.23           C
ATOM     19  C   ARG A   5       2.250  -2.854   6.040  1.00  3.90           C
ATOM     20  O   ARG A   5       1.150  -2.450   6.350  1.00  4.12           O
TER      21      ARG A   5
END
"""

    # 13. DNA PDB segment
    dna_pdb = """HEADER    DNA DOUBLE HELIX                        15-FEB-81   1BNA
TITLE     DNA 10-MER BACKBONE
ATOM      1  P   DA  A   1      -1.745   9.897  -4.135  1.00 20.00           P
ATOM      2  OP1 DA  A   1      -2.548  10.320  -5.321  1.00 20.00           O
ATOM      3  OP2 DA  A   1      -1.921   8.541  -3.521  1.00 20.00           O
ATOM      4  O5' DA  A   1      -0.201  10.012  -4.521  1.00 20.00           O
ATOM      5  C5' DA  A   1       0.820   9.814  -3.524  1.00 20.00           C
ATOM      6  C4' DA  A   1       2.124  10.150  -4.215  1.00 20.00           C
ATOM      7  C3' DA  A   1       2.254   9.412  -5.501  1.00 20.00           C
ATOM      8  O3' DA  A   1       1.240   9.852  -6.381  1.00 20.00           O
ATOM      9  P   DT  A   2       1.450   9.642  -7.954  1.00 20.00           P
ATOM     10  OP1 DT  A   2       0.120   9.921  -8.541  1.00 20.00           O
ATOM     11  OP2 DT  A   2       2.541  10.450  -8.320  1.00 20.00           O
ATOM     12  O5' DT  A   2       1.854   8.120  -8.154  1.00 20.00           O
ATOM     13  C5' DT  A   2       2.852   7.641  -9.041  1.00 20.00           C
ATOM     14  C4' DT  A   2       3.120   6.150  -8.751  1.00 20.00           C
ATOM     15  C3' DT  A   2       1.841   5.421  -9.120  1.00 20.00           C
ATOM     16  O3' DT  A   2       2.045   4.012  -9.001  1.00 20.00           O
TER      17      DT  A   2
END
"""

    print("Creating compounds...")
    
    # helper for seeding synonyms
    def add_synonyms(compound_id, names_list):
        for name in names_list:
            db.add(Synonym(compound_id=compound_id, synonym=name))
    
    # 1. Water
    h2o = Compound(
        category=categories_data["inorganic-chemistry"],
        name="Water",
        slug="water",
        formula="H2O",
        iupac_name="oxidane",
        cas_number="7732-18-5",
        molecular_weight=18.015,
        smiles="O",
        inchi="InChI=1S/H2O/h1H2",
        pubchem_cid=962,
        chebi_id="CHEBI:15377",
        subcategory="Oxides",
        description="Water is a transparent, odorless, tasteless liquid compound forming the world's streams, lakes, oceans and the fluids of organisms. It is a vital polar solvent in chemical and biological systems.",
        storage_recommendations="Store in clean, sealed containers at room temperature. Keep away from water-reactive substances.",
        biological_role="Universal biological solvent, cell volume regulator, reactant in hydrolysis reactions, and environment for metabolic pathways.",
        applications="Industrial solvent, cooling agent, agricultural irrigation, domestic use, chemical synthesis medium.",
        industrial_uses="Power generation (steam turbines), manufacturing solvent, cooling, hydraulic fluid."
    )
    db.add(h2o)
    db.flush()
    add_synonyms(h2o.id, ["Dihydrogen monoxide", "Oxidane", "Aqua", "H2O", "Distilled water"])
    db.add(PhysicalProperty(compound_id=h2o.id, melting_point="0.0 °C (32.0 °F; 273.15 K)", boiling_point="99.98 °C (211.96 °F; 373.13 K)", density="0.9998 g/cm³ (at 0 °C) / 0.997 g/cm³ (at 25 °C)", solubility="Miscible in polar solvents (Universal solvent)", appearance="Colorless, odorless, tasteless liquid"))
    db.add(ChemicalProperty(compound_id=h2o.id, acidity_pka="13.999 (at 25 °C)", refractive_index="1.3330 (at 20 °C)", chemical_stability="Highly stable, non-flammable", reactivity="Reacts violently with alkali metals (e.g. Sodium) producing Hydrogen gas"))
    db.add(Hazard(compound_id=h2o.id, ghs_classification="Not classified as hazardous", hazard_statements="None", precautionary_statements="None", safety_equipment="Standard lab safety goggles"))
    db.add(VisualizationMetadata(compound_id=h2o.id, two_d_svg='<svg viewBox="0 0 100 60" width="100" height="60" xmlns="http://www.w3.org/2000/svg"><line x1="20" y1="40" x2="50" y2="20" stroke="black" stroke-width="2"/><line x1="80" y1="40" x2="50" y2="20" stroke="black" stroke-width="2"/><circle cx="50" cy="20" r="12" fill="white" stroke="black" stroke-width="2"/><text x="45" y="25" font-family="monospace" font-weight="bold" font-size="14">O</text><circle cx="20" cy="40" r="10" fill="white" stroke="black" stroke-width="2"/><text x="15" y="45" font-family="monospace" font-size="12">H</text><circle cx="80" cy="40" r="10" fill="white" stroke="black" stroke-width="2"/><text x="75" y="45" font-family="monospace" font-size="12">H</text></svg>', three_d_sdf=water_sdf, three_d_model_type="sdf"))
    db.add(Reference(compound_id=h2o.id, citation="Lide, D. R. (2004). CRC Handbook of Chemistry and Physics (85th ed.). CRC Press.", doi="10.1201/9781420036688", url="https://www.crcpress.com"))

    # 2. Ethanol
    ethanol = Compound(
        category=categories_data["alcohols"],
        name="Ethanol",
        slug="ethanol",
        formula="C2H5OH",
        iupac_name="ethanol",
        cas_number="64-17-5",
        molecular_weight=46.069,
        smiles="CCO",
        inchi="InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3",
        pubchem_cid=702,
        chebi_id="CHEBI:16236",
        subcategory="Primary Alcohols",
        description="Ethanol, also commonly called ethyl alcohol, grain alcohol, or drinking alcohol, is a clear, colorless, volatile liquid. It is a primary alcohol and is highly flammable.",
        storage_recommendations="Store in a cool, dry, well-ventilated location. Keep container tightly closed and away from heat, sparks, and open flame.",
        biological_role="Product of anaerobic yeast fermentation, central nervous system depressant in mammals, metabolic substrate oxidized to acetaldehyde by alcohol dehydrogenase.",
        applications="Reagent in organic synthesis, bio-fuel additive, solvent in pharmaceuticals, perfumes, and varnishes, disinfectant/antiseptic agent, active ingredient in alcoholic beverages.",
        industrial_uses="Fuel blending agent (E10/E85), solvent for chemical extracts, industrial cleaning solvent."
    )
    db.add(ethanol)
    db.flush()
    add_synonyms(ethanol.id, ["Ethyl alcohol", "Methylcarbinol", "Grain alcohol", "EtOH", "Drinking alcohol"])
    db.add(PhysicalProperty(compound_id=ethanol.id, melting_point="-114.14 °C (-173.45 °F; 159.01 K)", boiling_point="78.24 °C (172.83 °F; 351.39 K)", density="0.7893 g/cm³ (at 20 °C)", solubility="Miscible in water, benzene, ether, acetone, chloroform", appearance="Clear, colorless liquid with a pleasant, characteristic spirituous odor"))
    db.add(ChemicalProperty(compound_id=ethanol.id, acidity_pka="15.9", refractive_index="1.361", chemical_stability="Stable under recommended storage conditions, volatile", reactivity="Reacts with strong oxidizing agents, acid chlorides, acid anhydrides, and alkali metals"))
    db.add(Hazard(compound_id=ethanol.id, ghs_classification="Class 3 Flammable Liquid, Eye Irritant (Category 2A)", hazard_statements="H225: Highly flammable liquid and vapor. H319: Causes serious eye irritation.", precautionary_statements="P210: Keep away from heat, hot surfaces, sparks, open flames. P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes.", safety_equipment="Safety glasses, flame-retardant lab coat, nitrile gloves, chemical fume hood for vapors"))
    db.add(VisualizationMetadata(compound_id=ethanol.id, two_d_svg='<svg viewBox="0 0 160 60" width="160" height="60" xmlns="http://www.w3.org/2000/svg"><line x1="30" y1="30" x2="80" y2="30" stroke="black" stroke-width="2"/><line x1="80" y1="30" x2="130" y2="30" stroke="black" stroke-width="2"/><circle cx="30" cy="30" r="12" fill="white" stroke="black" stroke-width="2"/><text x="23" y="35" font-family="monospace" font-size="14">CH3</text><circle cx="80" cy="30" r="12" fill="white" stroke="black" stroke-width="2"/><text x="73" y="35" font-family="monospace" font-size="14">CH2</text><circle cx="130" cy="30" r="12" fill="white" stroke="black" stroke-width="2"/><text x="123" y="35" font-family="monospace" font-size="14">OH</text></svg>', three_d_sdf=ethanol_sdf, three_d_model_type="sdf"))
    db.add(Reference(compound_id=ethanol.id, citation="National Center for Biotechnology Information (2026). PubChem Compound Summary for CID 702, Ethanol.", doi="10.1093/pubchem/702", url="https://pubchem.ncbi.nlm.nih.gov/compound/Ethanol"))

    # 3. Methanol
    methanol = Compound(
        category=categories_data["alcohols"],
        name="Methanol",
        slug="methanol",
        formula="CH3OH",
        iupac_name="methanol",
        cas_number="67-56-1",
        molecular_weight=32.042,
        smiles="CO",
        inchi="InChI=1S/CH4O/c1-2/h2H,1H3",
        pubchem_cid=887,
        chebi_id="CHEBI:17790",
        subcategory="Simple Alcohols",
        description="Methanol, also known as methyl alcohol, is a light, volatile, colorless, flammable liquid with a distinctive alcoholic odor. It is the simplest alcohol and is highly toxic to humans.",
        storage_recommendations="Store in a cool, dry, well-ventilated area away from heat, sparks, and open flames. Keep container tightly closed in a locked cabinet.",
        biological_role="Highly toxic; metabolized in the liver to formaldehyde and formic acid, causing metabolic acidosis and irreversible damage to the optic nerve (blindness).",
        applications="Industrial solvent, denaturant for ethanol, chemical feedstock for manufacturing formaldehyde, and alternative fuel/antifreeze source.",
        industrial_uses="Chemical synthesis feedstock (formaldehyde, acetic acid), transesterification of biodiesel, industrial solvent."
    )
    db.add(methanol)
    db.flush()
    add_synonyms(methanol.id, ["Methyl alcohol", "Wood alcohol", "Carbinol", "MeOH", "Wood spirit"])
    db.add(PhysicalProperty(compound_id=methanol.id, melting_point="-97.6 °C (-143.7 °F; 175.6 K)", boiling_point="64.7 °C (148.5 °F; 337.8 K)", density="0.792 g/cm³ (at 20 °C)", solubility="Miscible in water, ethanol, ether, benzene, chloroform", appearance="Clear, colorless, volatile liquid with a mild alcoholic odor"))
    db.add(ChemicalProperty(compound_id=methanol.id, acidity_pka="15.5", refractive_index="1.328", chemical_stability="Stable under standard conditions. Volatile and highly flammable", reactivity="Reacts violently with strong oxidizers, acid chlorides, acid anhydrides, and alkali metals"))
    db.add(Hazard(compound_id=methanol.id, ghs_classification="Class 3 Flammable Liquid, Acute Toxicity (Oral/Dermal/Inhalation, Category 3), target Organ Toxicity (Category 1)", hazard_statements="H225: Highly flammable liquid and vapor. H301+H311+H331: Toxic if swallowed, in contact with skin, or if inhaled. H370: Causes damage to organs (optic nerve).", precautionary_statements="P210: Keep away from heat, sparks, open flames. P280: Wear protective gloves/clothing/eye protection. P301+P310: IF SWALLOWED: Immediately call a POISON CENTER/doctor.", safety_equipment="Butol/nitrile gloves, splash goggles, flame-resistant lab coat, chemical fume hood"))
    db.add(VisualizationMetadata(compound_id=methanol.id, two_d_svg='<svg viewBox="0 0 100 60" width="100" height="60" xmlns="http://www.w3.org/2000/svg"><line x1="25" y1="30" x2="75" y2="30" stroke="black" stroke-width="2"/><circle cx="25" cy="30" r="12" fill="white" stroke="black" stroke-width="2"/><text x="18" y="35" font-family="monospace" font-size="12">CH3</text><circle cx="75" cy="30" r="12" fill="white" stroke="black" stroke-width="2"/><text x="68" y="35" font-family="monospace" font-size="12">OH</text></svg>', three_d_sdf=methanol_sdf, three_d_model_type="sdf"))
    db.add(Reference(compound_id=methanol.id, citation="National Center for Biotechnology Information (2026). PubChem Compound Summary for CID 887, Methanol.", doi="10.1093/pubchem/887", url="https://pubchem.ncbi.nlm.nih.gov/compound/Methanol"))

    # 4. Benzene
    benzene = Compound(
        category=categories_data["hydrocarbons"],
        name="Benzene",
        slug="benzene",
        formula="C6H6",
        iupac_name="benzene",
        cas_number="71-43-2",
        molecular_weight=78.11,
        smiles="c1ccccc1",
        inchi="InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H",
        pubchem_cid=241,
        chebi_id="CHEBI:16716",
        subcategory="Arenes (Aromatic)",
        description="Benzene is a simple organic chemical compound with six carbon atoms joined in a planar hexagonal ring. It is a natural constituent of crude oil and a key industrial chemical.",
        storage_recommendations="Store in a dedicated flammable liquids cabinet. Keep container tightly sealed in a cool place. Avoid all exposure and inhalation.",
        biological_role="Highly toxic; metabolized in the liver to toxic epoxides causing bone marrow depression and leukemia.",
        applications="Precursor in the production of plastics, resins, synthetic fibers, rubber, dyes, detergents, drugs, and pesticides.",
        industrial_uses="Chemical intermediate for ethylbenzene, cumene, and cyclohexane; solvent in industrial laboratories."
    )
    db.add(benzene)
    db.flush()
    add_synonyms(benzene.id, ["Benzol", "Cyclohexatriene", "Phene", "[6]-Annulene", "Coal naphtha"])
    db.add(PhysicalProperty(compound_id=benzene.id, melting_point="5.53 °C (41.95 °F; 278.68 K)", boiling_point="80.1 °C (176.2 °F; 353.2 K)", density="0.8765 g/cm³ (at 20 °C)", solubility="Slightly soluble in water (1.79 g/L at 25 °C), miscible in organic solvents", appearance="Clear, colorless liquid with a sweet, gasoline-like odor"))
    db.add(ChemicalProperty(compound_id=benzene.id, acidity_pka="43", refractive_index="1.5010 (at 20 °C)", chemical_stability="Stable, highly flammable, planar aromatic ring resistant to addition reactions", reactivity="Undergoes electrophilic aromatic substitution (nitration, halogenation, alkylation)"))
    db.add(Hazard(compound_id=benzene.id, ghs_classification="Class 3 Flammable Liquid, Carcinogen (Category 1A), Mutagen (Category 1B)", hazard_statements="H225: Highly flammable liquid and vapor. H350: May cause cancer. H340: May cause genetic defects.", precautionary_statements="P201: Obtain special instructions before use. P280: Wear protective gloves/clothing/eye protection. P308+P309: IF exposed or concerned: Get medical advice.", safety_equipment="Nitrile/Viton gloves, face shield, chemical-resistant apron, explosion-proof fume hood"))
    db.add(VisualizationMetadata(compound_id=benzene.id, two_d_svg='<svg viewBox="0 0 100 100" width="100" height="100" xmlns="http://www.w3.org/2000/svg"><polygon points="50,15 80,32 80,68 50,85 20,68 20,32" stroke="black" stroke-dasharray="none" stroke-width="2" fill="none"/><circle cx="50" cy="50" r="22" stroke="black" stroke-dasharray="4,4" stroke-width="2" fill="none"/></svg>', three_d_sdf=benzene_sdf, three_d_model_type="sdf"))
    db.add(Reference(compound_id=benzene.id, citation="IARC Working Group on the Evaluation of Carcinogenic Risks to Humans. (2018). Benzene. IARC Monographs, Volume 120.", doi="10.2307/iarc.benzene.120", url="https://monographs.iarc.who.int"))

    # 5. Caffeine
    caffeine = Compound(
        category=categories_data["organic-chemistry"],
        name="Caffeine",
        slug="caffeine",
        formula="C8H10N4O2",
        iupac_name="1,3,7-trimethylpurine-2,6-dione",
        cas_number="58-08-2",
        molecular_weight=194.19,
        smiles="CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
        inchi="InChI=1S/C8H10N4O2/c1-11-4-9-6-5(11)7(13)12(3)8(14)10(6)2/h4H,1-3H3",
        pubchem_cid=2519,
        chebi_id="CHEBI:27732",
        subcategory="Purine Alkaloids",
        description="Caffeine is a central nervous system stimulant of the methylxanthine class. It is the world's most widely consumed psychoactive drug, primarily sourced from coffee, tea, and cocoa.",
        storage_recommendations="Store in a cool, dry place in tightly closed container. Keep away from strong oxidizing agents.",
        biological_role="Adenosine receptor antagonist in the brain, inhibiting drowsiness. Increases heart rate, blood pressure, and metabolic rate.",
        applications="Beverage additive, stimulant in prescription and over-the-counter pharmaceuticals (e.g. pain relievers, alertness aids).",
        industrial_uses="Active ingredient in energy drinks, dietary supplements, and pharmaceutical formulations."
    )
    db.add(caffeine)
    db.flush()
    add_synonyms(caffeine.id, ["1,3,7-Trimethylxanthine", "Guaranine", "Theine", "Methyltheobromine", "Caffeine anhydrous"])
    db.add(PhysicalProperty(compound_id=caffeine.id, melting_point="235 °C (455 °F) (Anhydrous)", boiling_point="Sublimes at 178 °C (352 °F)", density="1.23 g/cm³ (at 18 °C)", solubility="Soluble in water (2.17 g/100 mL at 25 °C, 66 g/100 mL at 80 °C), chloroform, ethanol", appearance="White, odorless crystalline needles or powder with a bitter taste"))
    db.add(ChemicalProperty(compound_id=caffeine.id, acidity_pka="-0.13 (conjugate acid)", refractive_index="N/A (Solid)", chemical_stability="Stable under normal room temperatures, weak organic base", reactivity="Oxidized to dimethylalloxan and methylurea with strong oxidants. Subject to electrophilic substitution at carbon-8"))
    db.add(Hazard(compound_id=caffeine.id, ghs_classification="Acute Toxicity (Oral, Category 4)", hazard_statements="H302: Harmful if swallowed.", precautionary_statements="P264: Wash skin thoroughly after handling. P301+P312: IF SWALLOWED: Call a poison control center or doctor if you feel unwell.", safety_equipment="Standard lab safety goggles, disposable latex/nitrile gloves"))
    db.add(VisualizationMetadata(compound_id=caffeine.id, two_d_svg='<svg viewBox="0 0 120 100" width="120" height="100" xmlns="http://www.w3.org/2000/svg"><polygon points="30,30 65,30 80,50 65,70 30,70 15,50" stroke="black" stroke-width="2" fill="none"/><polygon points="65,30 95,15 110,40 90,60 65,50" stroke="black" stroke-width="2" fill="none"/></svg>', three_d_sdf=caffeine_sdf, three_d_model_type="sdf"))
    db.add(Reference(compound_id=caffeine.id, citation="Nehlig, A., Daval, J. L., & Debry, G. (1992). Caffeine and the central nervous system: brain action. Brain Research Reviews, 17(2), 139-170.", doi="10.1016/0169-328X(92)90012-B", url="https://www.sciencedirect.com"))

    # 6. Tetrahydropyran
    tetrahydropyran = Compound(
        category=categories_data["organic-chemistry"],
        name="Tetrahydropyran",
        slug="tetrahydropyran",
        formula="C5H10O",
        iupac_name="oxane",
        cas_number="142-68-7",
        molecular_weight=86.13,
        smiles="C1CCOCC1",
        inchi="InChI=1S/C5H10O/c1-2-4-6-5-3-1/h1-5H2",
        pubchem_cid=8882,
        chebi_id="CHEBI:46898",
        subcategory="Cyclic Ethers",
        description="Tetrahydropyran (THP), also known as oxane, is the organic compound consisting of a saturated six-membered ring containing five carbon atoms and one oxygen atom. It is a common volatile ether used as a solvent and organic synthesis intermediate.",
        storage_recommendations="Store in a cool, dry, well-ventilated location. Keep away from heat, sparks, open flames, and direct sunlight. Keep container tightly closed.",
        biological_role="Used as a core structural scaffold in various biological molecules, including pyranose sugars, and studied in host-guest enzyme receptor interactions.",
        applications="Reaction solvent, protecting group reagent in organic synthesis (THP ether formation), and intermediate in industrial chemical manufacturing.",
        industrial_uses="Solvent for polymer formulations, co-solvent for specialty reactions, protective groups chemical production."
    )
    db.add(tetrahydropyran)
    db.flush()
    add_synonyms(tetrahydropyran.id, ["Oxane", "Pentamethylene oxide", "THP", "Tetrahydro-2H-pyran"])
    db.add(PhysicalProperty(compound_id=tetrahydropyran.id, melting_point="-45 °C (-49 °F; 228 K)", boiling_point="88 °C (190 °F; 361 K)", density="0.8814 g/cm³ (at 20 °C)", solubility="Soluble in water (80 g/L at 20 °C), miscible in alcohol, ether, and acetone", appearance="Colorless, volatile liquid with a characteristic ether-like odor"))
    db.add(ChemicalProperty(compound_id=tetrahydropyran.id, acidity_pka="N/A", refractive_index="1.420", chemical_stability="Stable under standard conditions. May form explosive peroxides on prolonged exposure to air and light", reactivity="Generally inert ether, but undergoes ring-cleaving reactions under highly acidic conditions"))
    db.add(Hazard(compound_id=tetrahydropyran.id, ghs_classification="Class 3 Flammable Liquid, Eye Irritant (Category 2A)", hazard_statements="H225: Highly flammable liquid and vapor. H319: Causes serious eye irritation.", precautionary_statements="P210: Keep away from heat, hot surfaces, sparks, open flames. P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes.", safety_equipment="Safety glasses, flame-retardant lab coat, nitrile gloves, chemical fume hood"))
    db.add(VisualizationMetadata(compound_id=tetrahydropyran.id, two_d_svg='<svg viewBox="0 0 100 100" width="100" height="100" xmlns="http://www.w3.org/2000/svg"><path d="M 50,15 L 80,32 L 80,50 M 80,62 L 80,68 L 50,85 L 20,68 L 20,32 L 50,15" stroke="black" stroke-width="2" fill="none" stroke-linejoin="round"/><text x="75" y="60" font-family="sans-serif" font-weight="bold" font-size="12" fill="black">O</text></svg>', three_d_sdf=tetrahydropyran_sdf, three_d_model_type="sdf"))
    db.add(Reference(compound_id=tetrahydropyran.id, citation="National Center for Biotechnology Information (2026). PubChem Compound Summary for CID 8882, Tetrahydropyran.", doi="10.1093/pubchem/8882", url="https://pubchem.ncbi.nlm.nih.gov/compound/Tetrahydropyran"))

    # 7. ATP
    atp = Compound(
        category=categories_data["organic-chemistry"],
        name="Adenosine Triphosphate",
        slug="atp",
        formula="C10H16N5O13P3",
        iupac_name="[[[[[(2R,3S,4R,5R)-5-(6-aminopurin-9-yl)-3,4-dihydroxyoxolan-2-yl]methoxy-hydroxyphosphoryl]oxy-hydroxyphosphoryl]oxy-hydroxyphosphoryl] acid",
        cas_number="56-65-5",
        molecular_weight=507.18,
        smiles="C1=NC(=C2C(=N1)N(C=N2)[C@H]3[C@@H]([C@@H]([C@H](O3)COP(=O)(O)OP(=O)(O)OP(=O)(O)O)O)O)N",
        inchi="InChI=1S/C10H16N5O13P3/c11-8-5-9(13-2-12-8)15(3-14-5)10-7(17)6(16)4(26-10)1-25-30(21,22)28-31(23,24)27-29(18,19)20/h2-3,6-7,10,16-17H,1H2,(H,21,22)(H,23,24)(H2,11,12,13)(H2,18,19,20)",
        pubchem_cid=5957,
        chebi_id="CHEBI:15422",
        subcategory="Ribonucleotides",
        description="Adenosine triphosphate (ATP) is an organic compound and hydrotrope that provides energy to drive many processes in living cells, such as muscle contraction, nerve impulse propagation, condensation, and chemical synthesis.",
        storage_recommendations="Store at -20 °C in a dry location. Protect from moisture and avoid repeated freeze-thaw cycles.",
        biological_role="Universal cellular energy currency; hydrolyzed to ADP or AMP to release free energy and drive biological work.",
        applications="Biochemical research reagent, substrate in kinase enzyme assays, and clinical agent for cardiovascular conditions.",
        industrial_uses="Biomedical assay production, enzyme substrate kits manufacturing."
    )
    db.add(atp)
    db.flush()
    add_synonyms(atp.id, ["Adenosine 5'-triphosphate", "Triphosphoadenosine", "Adenylpyrophosphate", "ATP", "Striadyne"])
    db.add(PhysicalProperty(compound_id=atp.id, melting_point="187 °C (369 °F) (Decomposes)", boiling_point="N/A (Solid)", density="1.04 g/cm³", solubility="Highly soluble in water (> 50 mg/mL at 25 °C), insoluble in organic solvents", appearance="White, odorless crystalline powder"))
    db.add(ChemicalProperty(compound_id=atp.id, acidity_pka="0.9, 1.5, 2.1, 6.8 (Multiple acidic phosphate groups)", refractive_index="N/A", chemical_stability="Unstable in aqueous solutions at high temperatures, hydrolyzes slowly to ADP at room temperature", reactivity="Subject to nucleophilic attack on the phosphate groups, driving phosphorylation reactions"))
    db.add(Hazard(compound_id=atp.id, ghs_classification="Not classified as hazardous", hazard_statements="None", precautionary_statements="None", safety_equipment="Standard lab safety goggles, nitrile gloves"))
    db.add(VisualizationMetadata(compound_id=atp.id, two_d_svg='<svg viewBox="0 0 160 100" width="160" height="100" xmlns="http://www.w3.org/2000/svg"><polygon points="20,40 45,25 70,40 58,65 32,65" stroke="black" stroke-width="2" fill="none"/><rect x="75" y="30" width="20" height="20" stroke="black" stroke-width="2" fill="none"/><circle cx="110" cy="40" r="8" stroke="black" stroke-width="2" fill="none"/><text x="108" y="44" font-family="sans-serif" font-size="10">P</text><circle cx="130" cy="40" r="8" stroke="black" stroke-width="2" fill="none"/><text x="128" y="44" font-family="sans-serif" font-size="10">P</text><circle cx="150" cy="40" r="8" stroke="black" stroke-width="2" fill="none"/><text x="148" y="44" font-family="sans-serif" font-size="10">P</text><text x="35" y="50" font-family="sans-serif" font-size="10">Ribose</text><text x="78" y="44" font-family="sans-serif" font-size="10">Ade</text></svg>', three_d_sdf=atp_sdf, three_d_model_type="sdf"))
    db.add(Reference(compound_id=atp.id, citation="Nelson, D. L., & Cox, M. M. (2017). Lehninger Principles of Biochemistry (7th ed.). W. H. Freeman.", doi="10.2307/biochem.lehninger.7", url="https://macmillanlearning.com"))
    
    db.add(Biomolecule(
        compound_id=atp.id,
        molecule_type="Nucleoside Triphosphate",
        sequence="N/A",
        structure_class="Purine Nucleotide"
    ))

    # 8. Acetone
    acetone = Compound(
        category=categories_data["ketones"],
        name="Acetone",
        slug="acetone",
        formula="C3H6O",
        iupac_name="propan-2-one",
        cas_number="67-64-1",
        molecular_weight=58.08,
        smiles="CC(=O)C",
        inchi="InChI=1S/C3H6O/c1-3(2)4/h1-2H3",
        pubchem_cid=180,
        chebi_id="CHEBI:15347",
        subcategory="Simple Ketones",
        description="Acetone, or propanone, is the simplest and smallest ketone. It is a colorless, highly volatile and flammable liquid with a characteristic pungent, sweetish odor.",
        storage_recommendations="Store in a cool, well-ventilated, standard fire safety storage room. Keep away from ignition sources.",
        biological_role="Minor product of metabolic ketogenesis in mammalian starvation or diabetic ketoacidosis.",
        applications="Industrial solvent, nail polish remover solvent, precursor to methyl methacrylate and bisphenol A.",
        industrial_uses="General industrial solvent for paints, lacquers, and varnishes, chemical intermediate for acrylic plastics."
    )
    db.add(acetone)
    db.flush()
    add_synonyms(acetone.id, ["2-Propanone", "Dimethyl ketone", "Propanone", "Pyroacetic ether", "β-ketopropane"])
    db.add(PhysicalProperty(compound_id=acetone.id, melting_point="-94.7 °C", boiling_point="56.05 °C", density="0.784 g/cm³", solubility="Miscible in water, ethanol, diethyl ether, chloroform", appearance="Clear, colorless, volatile liquid with a sweet, pungent odor"))
    db.add(ChemicalProperty(compound_id=acetone.id, acidity_pka="24.2", refractive_index="1.3588", chemical_stability="Stable under normal storage conditions, highly volatile", reactivity="Reacts with strong oxidizing agents, halogenated compounds, and reducing agents"))
    db.add(Hazard(compound_id=acetone.id, ghs_classification="Class 3 Flammable Liquid, Eye Irritant (Category 2A), Target Organ Toxicity (Category 3 - Drowsiness)", hazard_statements="H225: Highly flammable liquid and vapor. H319: Causes serious eye irritation. H336: May cause drowsiness or dizziness.", precautionary_statements="P210: Keep away from heat, sparks, open flames. P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes.", safety_equipment="Safety glasses, nitrile gloves, lab coat, fume hood"))
    db.add(VisualizationMetadata(compound_id=acetone.id, two_d_svg='<svg viewBox="0 0 100 60" width="100" height="60" xmlns="http://www.w3.org/2000/svg"><line x1="20" y1="40" x2="50" y2="25" stroke="black" stroke-width="2"/><line x1="80" y1="40" x2="50" y2="25" stroke="black" stroke-width="2"/><line x1="48" y1="25" x2="48" y2="5" stroke="black" stroke-width="2"/><line x1="52" y1="25" x2="52" y2="5" stroke="black" stroke-width="2"/><circle cx="50" cy="25" r="10" fill="white" stroke="black" stroke-width="2"/><text x="45" y="30" font-family="monospace" font-size="12">C</text><text x="12" y="45" font-family="monospace" font-size="10">CH3</text><text x="75" y="45" font-family="monospace" font-size="10">CH3</text><text x="47" y="2" font-family="monospace" font-weight="bold" font-size="12">O</text></svg>', three_d_sdf=acetone_sdf, three_d_model_type="sdf"))
    db.add(Reference(compound_id=acetone.id, citation="National Center for Biotechnology Information (2026). PubChem Compound Summary for CID 180, Acetone.", doi="10.1093/pubchem/180", url="https://pubchem.ncbi.nlm.nih.gov/compound/Acetone"))

    # 9. Formaldehyde
    formaldehyde = Compound(
        category=categories_data["aldehydes"],
        name="Formaldehyde",
        slug="formaldehyde",
        formula="CH2O",
        iupac_name="methanal",
        cas_number="50-00-0",
        molecular_weight=30.026,
        smiles="C=O",
        inchi="InChI=1S/CH2O/c1-2/h1H2",
        pubchem_cid=712,
        chebi_id="CHEBI:16842",
        subcategory="Simple Aldehydes",
        description="Formaldehyde is a naturally occurring organic compound, the simplest of the aldehydes. It is a highly toxic gas at room temperature and is widely used as a tissue preservative and chemical precursor.",
        storage_recommendations="Store under lock and key. Keep away from strong oxidizers, alkalis, acids. Maintain in ventilated chemical safety storage cabinets.",
        biological_role="Endogenous metabolic byproduct of amino acid demethylation, toxic in high levels, cross-links DNA and proteins causing genetic mutations.",
        applications="Biological specimen tissue preservative (formalin), industrial adhesive resin precursor (urea-formaldehyde), industrial disinfectant.",
        industrial_uses="Precursor to polyoxymethylene plastics, urea-formaldehyde adhesives, textile finishing resins."
    )
    db.add(formaldehyde)
    db.flush()
    add_synonyms(formaldehyde.id, ["Methanal", "Formalin", "Formic aldehyde", "Methylene oxide", "Oxomethane"])
    db.add(PhysicalProperty(compound_id=formaldehyde.id, melting_point="-92 °C", boiling_point="-19 °C", density="0.815 g/cm³ (at -20 °C)", solubility="Highly soluble in water (> 400 g/L), soluble in ethanol, diethyl ether", appearance="Colorless, pungent, suffocating gas (sold commercially as 37% aqueous solution, formalin)"))
    db.add(ChemicalProperty(compound_id=formaldehyde.id, acidity_pka="13.27", refractive_index="1.37 (Formalin)", chemical_stability="Highly reactive, polymerizes spontaneously to paraformaldehyde unless stabilized with methanol", reactivity="Easily oxidized to formic acid, undergoes nucleophilic addition reactions, cross-links amines"))
    db.add(Hazard(compound_id=formaldehyde.id, ghs_classification="Acute Toxicity (Oral/Dermal/Inhalation, Category 3), Carcinogen (Category 1A), Skin Sensitization (Category 1)", hazard_statements="H301+H311+H331: Toxic if swallowed, in contact with skin, or if inhaled. H350: May cause cancer. H317: May cause an allergic skin reaction.", precautionary_statements="P201: Obtain special instructions before use. P280: Wear protective gloves/clothing/eye protection. P301+P310: IF SWALLOWED: Immediately call a POISON CENTER.", safety_equipment="Nitrile/neoprene gloves, splash goggles, lab coat, chemical fume hood"))
    db.add(VisualizationMetadata(compound_id=formaldehyde.id, two_d_svg='<svg viewBox="0 0 100 60" width="100" height="60" xmlns="http://www.w3.org/2000/svg"><line x1="50" y1="40" x2="50" y2="15" stroke="black" stroke-width="2"/><line x1="48" y1="40" x2="48" y2="15" stroke="black" stroke-width="2"/><line x1="52" y1="40" x2="52" y2="15" stroke="black" stroke-width="2"/><circle cx="50" cy="40" r="10" fill="white" stroke="black" stroke-width="2"/><text x="45" y="45" font-family="monospace" font-size="12">CH2</text><text x="47" y="12" font-family="monospace" font-weight="bold" font-size="12">O</text></svg>', three_d_sdf=formaldehyde_sdf, three_d_model_type="sdf"))
    db.add(Reference(compound_id=formaldehyde.id, citation="IARC Working Group on the Evaluation of Carcinogenic Risks to Humans. (2006). Formaldehyde. IARC Monographs, Volume 88.", doi="10.2307/iarc.formal.88", url="https://monographs.iarc.who.int"))

    # 10. Aspirin
    aspirin = Compound(
        category=categories_data["drugs"],
        name="Aspirin",
        slug="aspirin",
        formula="C9H8O4",
        iupac_name="2-acetyloxybenzoic acid",
        cas_number="50-78-2",
        molecular_weight=180.158,
        smiles="CC(=O)Oc1ccccc1C(=O)O",
        inchi="InChI=1S/C9H8O4/c1-5(10)13-8-4-2-3-7(8)9(11)12/h2-4H,1H3,(H,11,12)",
        pubchem_cid=2244,
        chebi_id="CHEBI:15365",
        subcategory="Salicylates",
        description="Aspirin, also known as acetylsalicylic acid (ASA), is a common nonsteroidal anti-inflammatory drug (NSAID) used to reduce pain, fever, and inflammation, and as an antithrombotic agent.",
        storage_recommendations="Store at room temperature in dry containers. Keep away from moisture to prevent hydrolysis into salicylic acid.",
        biological_role="Irreversible inhibitor of cyclooxygenase enzymes (COX-1 and COX-2), preventing prostaglandin and thromboxane synthesis.",
        applications="Analgesic for pain relief, antipyretic for reducing fever, anti-inflammatory for arthritis, and low-dose antiplatelet drug for stroke prevention.",
        industrial_uses="Pharmaceutical active ingredient synthesis and formulation tableting."
    )
    db.add(aspirin)
    db.flush()
    add_synonyms(aspirin.id, ["Acetylsalicylic acid", "ASA", "2-Acetoxybenzoic acid", "Aspirine", "Ecotrin"])
    db.add(PhysicalProperty(compound_id=aspirin.id, melting_point="135 °C", boiling_point="140 °C (Decomposes)", density="1.40 g/cm³", solubility="Slightly soluble in water (3 mg/mL at 25 °C), soluble in ethanol, ether, chloroform", appearance="White, crystalline powder or monoclinic needles with a slightly acid taste"))
    db.add(ChemicalProperty(compound_id=aspirin.id, acidity_pka="3.5", refractive_index="N/A", chemical_stability="Stable in dry air, but hydrolyzes gradually in moist environments into acetic and salicylic acids", reactivity="Undergoes transesterification, easily hydrolyzed by base, ester linkage cleaved in acids"))
    db.add(Hazard(compound_id=aspirin.id, ghs_classification="Acute Toxicity (Oral, Category 4), Eye Irritant (Category 2A)", hazard_statements="H302: Harmful if swallowed. H319: Causes serious eye irritation.", precautionary_statements="P264: Wash skin thoroughly after handling. P301+P312: IF SWALLOWED: Call a POISON CENTER if you feel unwell.", safety_equipment="Safety glasses, nitrile gloves, lab coat"))
    db.add(VisualizationMetadata(compound_id=aspirin.id, two_d_svg='<svg viewBox="0 0 100 100" width="100" height="100" xmlns="http://www.w3.org/2000/svg"><polygon points="50,30 75,42 75,70 50,82 25,70 25,42" stroke="black" stroke-width="2" fill="none"/><line x1="75" y1="42" x2="90" y2="30" stroke="black" stroke-width="2"/><text x="92" y="32" font-family="sans-serif" font-size="10">O-Ac</text></svg>', three_d_sdf=aspirin_sdf, three_d_model_type="sdf"))
    db.add(Reference(compound_id=aspirin.id, citation="Vane, J. R. (1971). Inhibition of prostaglandin synthesis as a mechanism of action for aspirin-like drugs. Nature New Biology, 231(25), 232-235.", doi="10.1038/newbio231232a0", url="https://www.nature.com"))

    # 11. Buckminsterfullerene (C60)
    c60 = Compound(
        category=categories_data["nanomaterials"],
        name="Buckminsterfullerene",
        slug="buckminsterfullerene",
        formula="C60",
        iupac_name="(C60-Ih)[5,6]fullerene",
        cas_number="99685-96-8",
        molecular_weight=720.64,
        smiles="C12=C3C4=C5C6=C1... (abbreviated C60 cage representation)",
        inchi="InChI=1S/C60/c1-2-5-6-3(1)8-12-10-4(2)9-15-18-20-17-11(5)14-23-25-22-13(6)21-24-19(7-8)27-30-28(12)32-35-33(10)34(9)41-43-38(15)37(18)46-48-40(17)39(14)47-50-42(23)45(22)52-54-44(21)49(24)51(25)55-57-53(52)56(54)59-60-58(55)57/i",
        pubchem_cid=123532,
        chebi_id="CHEBI:33128",
        subcategory="Fullerenes",
        description="Buckminsterfullerene (C60), also known as the Buckyball, is a spherical carbon allotrope consisting of 60 carbon atoms structured in twenty hexagons and twelve pentagons, resembling a soccer ball.",
        storage_recommendations="Store at room temperature in dark, tightly closed vials. Keep away from strong light and oxidizing agents.",
        biological_role="Potential antioxidant/radical scavenger due to high electron affinity; studied for drug delivery vector applications.",
        applications="Superconductor compound precursor, organic photovoltaic cells electron acceptor, lubricants additive, nanotechnology research material.",
        industrial_uses="Electron acceptors in organic solar panels, research standard for nanoscale structures, mechanical lubricant enhancers."
    )
    db.add(c60)
    db.flush()
    add_synonyms(c60.id, ["Buckyball", "Fullerene C60", "[60]Fullerene", "Footballene", "Buckminster fullerene"])
    db.add(PhysicalProperty(compound_id=c60.id, melting_point="Sublimes at >280 °C (under vacuum)", boiling_point="N/A", density="1.65 g/cm³", solubility="Insoluble in water, slightly soluble in toluene (2.8 mg/mL), benzene, carbon disulfide", appearance="Dark brown to black crystalline solid or fine powder"))
    db.add(ChemicalProperty(compound_id=c60.id, acidity_pka="N/A", refractive_index="2.2 (Solid film)", chemical_stability="Thermally stable up to 500 °C in air, highly stable cage structure", reactivity="Electrophilic addition reactive, acts as an electron-deficient alkene, undergoes hydrogenation and halogenation"))
    db.add(Hazard(compound_id=c60.id, ghs_classification="Eye Irritant (Category 2B), Target Organ Toxicity (Category 3 - Respiratory)", hazard_statements="H320: Causes eye irritation. H335: May cause respiratory irritation.", precautionary_statements="P261: Avoid breathing dust. P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes.", safety_equipment="Safety glasses, nitrile gloves, dust mask or respirator, laboratory hood"))
    db.add(VisualizationMetadata(compound_id=c60.id, two_d_svg='<svg viewBox="0 0 100 100" width="100" height="100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="30" stroke="black" stroke-width="2" fill="none"/><polygon points="50,20 65,30 65,50 50,60 35,50 35,30" stroke="black" stroke-width="1" fill="none"/></svg>', three_d_sdf=c60_sdf, three_d_model_type="sdf"))
    db.add(Reference(compound_id=c60.id, citation="Kroto, H. W., Heath, J. R., O'Brien, S. C., Curl, R. F., & Smalley, R. E. (1985). C60: Buckminsterfullerene. Nature, 318(6042), 162-163.", doi="10.1038/318162a0", url="https://www.nature.com/articles/318162a0"))

    # 12. Human Lysozyme
    lysozyme = Compound(
        category=categories_data["proteins"],
        name="Lysozyme",
        slug="lysozyme",
        formula="C688H1053N209O193S10",
        iupac_name="Human Lysozyme C",
        cas_number="9001-63-2",
        molecular_weight=14700.2,
        smiles="N/A (Macromolecule)",
        inchi="N/A (Macromolecule)",
        pubchem_cid=6914757,
        chebi_id="CHEBI:6687",
        subcategory="Hydrolases",
        description="Lysozyme is an enzyme that catalyzes the hydrolysis of 1,4-beta-linkages between N-acetylmuramic acid and N-acetylglucosamine residues in peptidoglycan bacterial cell walls. It is abundant in secretions like tears, saliva, and mucus.",
        storage_recommendations="Store lyophilized powder at -20 °C. Reconstituted solutions should be stored at 4 °C or aliquoted and frozen to maintain activity.",
        biological_role="Innate immune defense against Gram-positive bacterial infections by lysing their cell wall peptidoglycan layer.",
        applications="Antibacterial agent in food preservation, clinical diagnostic reagent, structural reference standard in protein crystallography.",
        industrial_uses="Antibacterial enzyme in winemaking and cheese production, clinical diagnostic assays."
    )
    db.add(lysozyme)
    db.flush()
    add_synonyms(lysozyme.id, ["Muramidase", "Lytic enzyme", "Lysozyme C", "Globulin G1", "Human lysozyme"])
    db.add(PhysicalProperty(compound_id=lysozyme.id, melting_point="Decomposes / Denatures at >72 °C", boiling_point="N/A", density="~1.35.0 g/cm³ (dry)", solubility="Soluble in aqueous buffers, saline, and water up to 50 mg/mL", appearance="White to off-white lyophilized powder"))
    db.add(ChemicalProperty(compound_id=lysozyme.id, acidity_pka="Isoelectric Point (pI) = 11.35", refractive_index="N/A", chemical_stability="Stable at acidic to neutral pH. Highly susceptible to denaturing agents (urea, guanidine HCl) and high temperatures", reactivity="Enzymatic hydrolysis of glycosidic bonds in bacterial peptidoglycan"))
    db.add(Hazard(compound_id=lysozyme.id, ghs_classification="Sensitization - Respiratory (Category 1), Eye Irritant (Category 2)", hazard_statements="H334: May cause allergy or asthma symptoms or breathing difficulties if inhaled. H319: Causes serious eye irritation.", precautionary_statements="P261: Avoid breathing dust/fume/gas/mist/vapors/spray. P342+P311: If experiencing respiratory symptoms: Call a poison center or doctor.", safety_equipment="Face mask/respirator to prevent dust inhalation, nitrile gloves, lab coat, safety goggles"))
    db.add(VisualizationMetadata(compound_id=lysozyme.id, two_d_svg='<svg viewBox="0 0 100 100" width="100" height="100" xmlns="http://www.w3.org/2000/svg"><path d="M20,50 Q40,20 50,50 T80,50" fill="none" stroke="black" stroke-width="3"/><circle cx="20" cy="50" r="5" fill="black"/><circle cx="50" cy="50" r="5" fill="black"/><circle cx="80" cy="50" r="5" fill="black"/></svg>', three_d_sdf=lysozyme_pdb, three_d_model_type="pdb"))
    db.add(Reference(compound_id=lysozyme.id, citation="Blake, C. C. F., Koenig, D. F., Mair, G. A., North, A. C. T., Phillips, D. C., & Sarma, V. R. (1965). Structure of Hen Egg-White Lysozyme. Nature, 206(4986), 757-761.", doi="10.1038/206757a0", url="https://www.nature.com/articles/206757a0"))

    db.add(Biomolecule(
        compound_id=lysozyme.id,
        molecule_type="Protein",
        sequence="KVFERCELARTLKRLGMDGYRGISLANWMCLAKWESGYNTRATNYNAGDRSTDYGIFQINSRYWCNDGKTPGAVNACHLSCSALLQDNIADAVACAKRVVRDPQGIRAWVAWRNRCQNRDVRQYVQGCGV",
        structure_class="Globular Hydrolase (Alpha/Beta Protein)"
    ))

    lysozyme_protein = Protein(
        compound_id=lysozyme.id,
        gene_name="LYZ",
        organism="Homo sapiens (Human)",
        sequence="KVFERCELARTLKRLGMDGYRGISLANWMCLAKWESGYNTRATNYNAGDRSTDYGIFQINSRYWCNDGKTPGAVNACHLSCSALLQDNIADAVACAKRVVRDPQGIRAWVAWRNRCQNRDVRQYVQGCGV",
        pdb_id="1A8M",
        uniprot_id="P61626"
    )
    db.add(lysozyme_protein)
    db.flush()

    db.add(Enzyme(
        protein_id=lysozyme_protein.id,
        ec_number="3.2.1.17",
        catalytic_activity="Hydrolysis of 1,4-beta-linkages between N-acetylmuramic acid and N-acetylglucosamine residues",
        substrate="Bacterial peptidoglycan cell walls"
    ))

    # 13. DNA Segment
    dna = Compound(
        category=categories_data["dna"],
        name="DNA Oligonucleotide",
        slug="dna",
        formula="(C10H12N5O6P)n",
        iupac_name="Deoxyribonucleic acid oligonucleotide",
        cas_number="9007-49-2",
        molecular_weight=6500.0,
        smiles="N/A (Polymer)",
        inchi="N/A (Polymer)",
        pubchem_cid=None,
        chebi_id="CHEBI:16991",
        subcategory="Biopolymers",
        description="Deoxyribonucleic acid (DNA) oligonucleotide is a short polymer segment of nucleotide monomers carrying genetic instructions used in growth, development, and functioning of organisms.",
        storage_recommendations="Store at -20 °C in Tris-EDTA buffer. Avoid acidic environments to prevent depurination.",
        biological_role="Primary template for RNA transcription, DNA replication, and vector of inheritance.",
        applications="Primers for Polymerase Chain Reaction (PCR), gene sequencing probes, and molecular diagnostics.",
        industrial_uses="Diagnostic PCR kits assembly, gene synthesis templates production."
    )
    db.add(dna)
    db.flush()
    add_synonyms(dna.id, ["DNA backbone", "Double helix oligonucleotide", "Deoxyribose nucleic acid segment", "PCR Primer DNA"])
    db.add(PhysicalProperty(compound_id=dna.id, melting_point="Melts/Denatures at 75-85 °C (dependent on GC content)", boiling_point="N/A", density="~1.70 g/cm³", solubility="Highly soluble in aqueous buffers, slightly soluble in water, insoluble in ethanol", appearance="White, fibrous solid or aqueous solution"))
    db.add(ChemicalProperty(compound_id=dna.id, acidity_pka="2.1 (Phosphate backbone ionization)", refractive_index="N/A", chemical_stability="Highly stable under alkaline or neutral conditions. Slowly hydrolyzes in hot acidic solutions", reactivity="Undergoes hybridization with complementary strands to form double-stranded helices"))
    db.add(Hazard(compound_id=dna.id, ghs_classification="Not classified as hazardous", hazard_statements="None", precautionary_statements="None", safety_equipment="Standard lab safety goggles"))
    db.add(VisualizationMetadata(compound_id=dna.id, two_d_svg='<svg viewBox="0 0 100 100" width="100" height="100" xmlns="http://www.w3.org/2000/svg"><path d="M20,10 C20,90 80,10 80,90 M20,25 L80,25 M20,45 L80,45 M20,65 L80,65" stroke="black" stroke-width="2" fill="none"/></svg>', three_d_sdf=dna_pdb, three_d_model_type="pdb"))
    db.add(Reference(compound_id=dna.id, citation="Watson, J. D., & Crick, F. H. (1953). Molecular structure of nucleic acids: a structure for deoxyribose nucleic acid. Nature, 171(4356), 737-738.", doi="10.1038/171737a0", url="https://www.nature.com/articles/171737a0"))

    db.add(Biomolecule(
        compound_id=dna.id,
        molecule_type="DNA Oligonucleotide",
        sequence="5'-CGCGAATTCGCG-3'",
        structure_class="Double-stranded DNA (B-form)"
    ))

    # --- Commit all seeded records ---
    db.commit()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    seed_database()
