-- ========================================================
-- Aethera AI — Production PostgreSQL Data & Schema Dump
-- Generated for Path A Deployment (Railway / Neon / Supabase)
-- ========================================================

CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Table: categories (17 records)
INSERT INTO "categories" ("id", "name", "slug", "description") VALUES (1, 'Organic Chemistry', 'organic-chemistry', 'Compounds containing carbon covalently bonded to other elements, forming the basis of all life.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "categories" ("id", "name", "slug", "description") VALUES (2, 'Inorganic Chemistry', 'inorganic-chemistry', 'Chemical compounds that do not contain carbon-hydrogen bonds, including minerals and metals.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "categories" ("id", "name", "slug", "description") VALUES (3, 'Alcohols', 'alcohols', 'Organic compounds containing one or more hydroxyl (-OH) groups bound to a carbon atom.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "categories" ("id", "name", "slug", "description") VALUES (4, 'Acids', 'acids', 'Substances that donate hydrogen ions (protons) or accept electron pairs in chemical reactions.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "categories" ("id", "name", "slug", "description") VALUES (5, 'Bases', 'bases', 'Substances that accept protons, donate hydroxide ions, or release electrons in chemical reactions.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "categories" ("id", "name", "slug", "description") VALUES (6, 'Hydrocarbons', 'hydrocarbons', 'Organic compounds consisting entirely of hydrogen and carbon, such as alkanes, alkenes, and arenes.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "categories" ("id", "name", "slug", "description") VALUES (7, 'Ketones', 'ketones', 'Organic compounds containing a carbonyl functional group (C=O) bonded to two other carbon atoms.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "categories" ("id", "name", "slug", "description") VALUES (8, 'Aldehydes', 'aldehydes', 'Organic compounds containing a carbonyl group bonded to at least one hydrogen atom at the end of a carbon chain.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "categories" ("id", "name", "slug", "description") VALUES (9, 'Carbohydrates', 'carbohydrates', 'Biomolecules consisting of carbon, hydrogen, and oxygen atoms, including sugars, starch, and cellulose.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "categories" ("id", "name", "slug", "description") VALUES (10, 'Proteins', 'proteins', 'Large biomolecules composed of one or more long chains of amino acid residues.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "categories" ("id", "name", "slug", "description") VALUES (11, 'Enzymes', 'enzymes', 'Biological catalysts, almost always proteins, that accelerate chemical reactions in cells.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "categories" ("id", "name", "slug", "description") VALUES (12, 'Hormones', 'hormones', 'Signaling molecules produced by glands in multicellular organisms that regulate physiology and behavior.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "categories" ("id", "name", "slug", "description") VALUES (13, 'Lipids', 'lipids', 'Hydrophobic or amphiphilic biological molecules, including fats, waxes, sterols, and fat-soluble vitamins.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "categories" ("id", "name", "slug", "description") VALUES (14, 'DNA', 'dna', 'Deoxyribonucleic acid, the hereditary material in humans and almost all other organisms.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "categories" ("id", "name", "slug", "description") VALUES (15, 'RNA', 'rna', 'Ribonucleic acid, essential for coding, decoding, regulation, and expression of genes.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "categories" ("id", "name", "slug", "description") VALUES (16, 'Drugs', 'drugs', 'Chemical substances used to treat, cure, prevent, or diagnose a disease or to promote physical well-being.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "categories" ("id", "name", "slug", "description") VALUES (17, 'Nanomaterials', 'nanomaterials', 'Materials characterized by an ultra-fine grain size or structural dimensions between 1 and 100 nanometers.') ON CONFLICT ("id") DO NOTHING;
SELECT setval(pg_get_serial_sequence('"categories"', 'id'), COALESCE(MAX(id), 1)) FROM "categories";

-- Table: compounds (13 records)
INSERT INTO "compounds" ("id", "category_id", "name", "slug", "formula", "iupac_name", "cas_number", "molecular_weight", "description", "storage_recommendations", "biological_role", "applications", "smiles", "inchi", "pubchem_cid", "chebi_id", "subcategory", "industrial_uses") VALUES (1, 2, 'Water', 'water', 'H2O', 'oxidane', '7732-18-5', 18.015, 'Water is a transparent, odorless, tasteless liquid compound forming the world''s streams, lakes, oceans and the fluids of organisms. It is a vital polar solvent in chemical and biological systems.', 'Store in clean, sealed containers at room temperature. Keep away from water-reactive substances.', 'Universal biological solvent, cell volume regulator, reactant in hydrolysis reactions, and environment for metabolic pathways.', 'Industrial solvent, cooling agent, agricultural irrigation, domestic use, chemical synthesis medium.', 'O', 'InChI=1S/H2O/h1H2', 962, 'CHEBI:15377', 'Oxides', 'Power generation (steam turbines), manufacturing solvent, cooling, hydraulic fluid.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "compounds" ("id", "category_id", "name", "slug", "formula", "iupac_name", "cas_number", "molecular_weight", "description", "storage_recommendations", "biological_role", "applications", "smiles", "inchi", "pubchem_cid", "chebi_id", "subcategory", "industrial_uses") VALUES (2, 3, 'Ethanol', 'ethanol', 'C2H5OH', 'ethanol', '64-17-5', 46.069, 'Ethanol, also commonly called ethyl alcohol, grain alcohol, or drinking alcohol, is a clear, colorless, volatile liquid. It is a primary alcohol and is highly flammable.', 'Store in a cool, dry, well-ventilated location. Keep container tightly closed and away from heat, sparks, and open flame.', 'Product of anaerobic yeast fermentation, central nervous system depressant in mammals, metabolic substrate oxidized to acetaldehyde by alcohol dehydrogenase.', 'Reagent in organic synthesis, bio-fuel additive, solvent in pharmaceuticals, perfumes, and varnishes, disinfectant/antiseptic agent, active ingredient in alcoholic beverages.', 'CCO', 'InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3', 702, 'CHEBI:16236', 'Primary Alcohols', 'Fuel blending agent (E10/E85), solvent for chemical extracts, industrial cleaning solvent.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "compounds" ("id", "category_id", "name", "slug", "formula", "iupac_name", "cas_number", "molecular_weight", "description", "storage_recommendations", "biological_role", "applications", "smiles", "inchi", "pubchem_cid", "chebi_id", "subcategory", "industrial_uses") VALUES (3, 3, 'Methanol', 'methanol', 'CH3OH', 'methanol', '67-56-1', 32.042, 'Methanol, also known as methyl alcohol, is a light, volatile, colorless, flammable liquid with a distinctive alcoholic odor. It is the simplest alcohol and is highly toxic to humans.', 'Store in a cool, dry, well-ventilated area away from heat, sparks, and open flames. Keep container tightly closed in a locked cabinet.', 'Highly toxic; metabolized in the liver to formaldehyde and formic acid, causing metabolic acidosis and irreversible damage to the optic nerve (blindness).', 'Industrial solvent, denaturant for ethanol, chemical feedstock for manufacturing formaldehyde, and alternative fuel/antifreeze source.', 'CO', 'InChI=1S/CH4O/c1-2/h2H,1H3', 887, 'CHEBI:17790', 'Simple Alcohols', 'Chemical synthesis feedstock (formaldehyde, acetic acid), transesterification of biodiesel, industrial solvent.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "compounds" ("id", "category_id", "name", "slug", "formula", "iupac_name", "cas_number", "molecular_weight", "description", "storage_recommendations", "biological_role", "applications", "smiles", "inchi", "pubchem_cid", "chebi_id", "subcategory", "industrial_uses") VALUES (4, 6, 'Benzene', 'benzene', 'C6H6', 'benzene', '71-43-2', 78.11, 'Benzene is a simple organic chemical compound with six carbon atoms joined in a planar hexagonal ring. It is a natural constituent of crude oil and a key industrial chemical.', 'Store in a dedicated flammable liquids cabinet. Keep container tightly sealed in a cool place. Avoid all exposure and inhalation.', 'Highly toxic; metabolized in the liver to toxic epoxides causing bone marrow depression and leukemia.', 'Precursor in the production of plastics, resins, synthetic fibers, rubber, dyes, detergents, drugs, and pesticides.', 'c1ccccc1', 'InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H', 241, 'CHEBI:16716', 'Arenes (Aromatic)', 'Chemical intermediate for ethylbenzene, cumene, and cyclohexane; solvent in industrial laboratories.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "compounds" ("id", "category_id", "name", "slug", "formula", "iupac_name", "cas_number", "molecular_weight", "description", "storage_recommendations", "biological_role", "applications", "smiles", "inchi", "pubchem_cid", "chebi_id", "subcategory", "industrial_uses") VALUES (5, 1, 'Caffeine', 'caffeine', 'C8H10N4O2', '1,3,7-trimethylpurine-2,6-dione', '58-08-2', 194.19, 'Caffeine is a central nervous system stimulant of the methylxanthine class. It is the world''s most widely consumed psychoactive drug, primarily sourced from coffee, tea, and cocoa.', 'Store in a cool, dry place in tightly closed container. Keep away from strong oxidizing agents.', 'Adenosine receptor antagonist in the brain, inhibiting drowsiness. Increases heart rate, blood pressure, and metabolic rate.', 'Beverage additive, stimulant in prescription and over-the-counter pharmaceuticals (e.g. pain relievers, alertness aids).', 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C', 'InChI=1S/C8H10N4O2/c1-11-4-9-6-5(11)7(13)12(3)8(14)10(6)2/h4H,1-3H3', 2519, 'CHEBI:27732', 'Purine Alkaloids', 'Active ingredient in energy drinks, dietary supplements, and pharmaceutical formulations.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "compounds" ("id", "category_id", "name", "slug", "formula", "iupac_name", "cas_number", "molecular_weight", "description", "storage_recommendations", "biological_role", "applications", "smiles", "inchi", "pubchem_cid", "chebi_id", "subcategory", "industrial_uses") VALUES (6, 1, 'Tetrahydropyran', 'tetrahydropyran', 'C5H10O', 'oxane', '142-68-7', 86.13, 'Tetrahydropyran (THP), also known as oxane, is the organic compound consisting of a saturated six-membered ring containing five carbon atoms and one oxygen atom. It is a common volatile ether used as a solvent and organic synthesis intermediate.', 'Store in a cool, dry, well-ventilated location. Keep away from heat, sparks, open flames, and direct sunlight. Keep container tightly closed.', 'Used as a core structural scaffold in various biological molecules, including pyranose sugars, and studied in host-guest enzyme receptor interactions.', 'Reaction solvent, protecting group reagent in organic synthesis (THP ether formation), and intermediate in industrial chemical manufacturing.', 'C1CCOCC1', 'InChI=1S/C5H10O/c1-2-4-6-5-3-1/h1-5H2', 8882, 'CHEBI:46898', 'Cyclic Ethers', 'Solvent for polymer formulations, co-solvent for specialty reactions, protective groups chemical production.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "compounds" ("id", "category_id", "name", "slug", "formula", "iupac_name", "cas_number", "molecular_weight", "description", "storage_recommendations", "biological_role", "applications", "smiles", "inchi", "pubchem_cid", "chebi_id", "subcategory", "industrial_uses") VALUES (7, 1, 'Adenosine Triphosphate', 'atp', 'C10H16N5O13P3', '[[[[[(2R,3S,4R,5R)-5-(6-aminopurin-9-yl)-3,4-dihydroxyoxolan-2-yl]methoxy-hydroxyphosphoryl]oxy-hydroxyphosphoryl]oxy-hydroxyphosphoryl] acid', '56-65-5', 507.18, 'Adenosine triphosphate (ATP) is an organic compound and hydrotrope that provides energy to drive many processes in living cells, such as muscle contraction, nerve impulse propagation, condensation, and chemical synthesis.', 'Store at -20 °C in a dry location. Protect from moisture and avoid repeated freeze-thaw cycles.', 'Universal cellular energy currency; hydrolyzed to ADP or AMP to release free energy and drive biological work.', 'Biochemical research reagent, substrate in kinase enzyme assays, and clinical agent for cardiovascular conditions.', 'C1=NC(=C2C(=N1)N(C=N2)[C@H]3[C@@H]([C@@H]([C@H](O3)COP(=O)(O)OP(=O)(O)OP(=O)(O)O)O)O)N', 'InChI=1S/C10H16N5O13P3/c11-8-5-9(13-2-12-8)15(3-14-5)10-7(17)6(16)4(26-10)1-25-30(21,22)28-31(23,24)27-29(18,19)20/h2-3,6-7,10,16-17H,1H2,(H,21,22)(H,23,24)(H2,11,12,13)(H2,18,19,20)', 5957, 'CHEBI:15422', 'Ribonucleotides', 'Biomedical assay production, enzyme substrate kits manufacturing.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "compounds" ("id", "category_id", "name", "slug", "formula", "iupac_name", "cas_number", "molecular_weight", "description", "storage_recommendations", "biological_role", "applications", "smiles", "inchi", "pubchem_cid", "chebi_id", "subcategory", "industrial_uses") VALUES (8, 7, 'Acetone', 'acetone', 'C3H6O', 'propan-2-one', '67-64-1', 58.08, 'Acetone, or propanone, is the simplest and smallest ketone. It is a colorless, highly volatile and flammable liquid with a characteristic pungent, sweetish odor.', 'Store in a cool, well-ventilated, standard fire safety storage room. Keep away from ignition sources.', 'Minor product of metabolic ketogenesis in mammalian starvation or diabetic ketoacidosis.', 'Industrial solvent, nail polish remover solvent, precursor to methyl methacrylate and bisphenol A.', 'CC(=O)C', 'InChI=1S/C3H6O/c1-3(2)4/h1-2H3', 180, 'CHEBI:15347', 'Simple Ketones', 'General industrial solvent for paints, lacquers, and varnishes, chemical intermediate for acrylic plastics.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "compounds" ("id", "category_id", "name", "slug", "formula", "iupac_name", "cas_number", "molecular_weight", "description", "storage_recommendations", "biological_role", "applications", "smiles", "inchi", "pubchem_cid", "chebi_id", "subcategory", "industrial_uses") VALUES (9, 8, 'Formaldehyde', 'formaldehyde', 'CH2O', 'methanal', '50-00-0', 30.026, 'Formaldehyde is a naturally occurring organic compound, the simplest of the aldehydes. It is a highly toxic gas at room temperature and is widely used as a tissue preservative and chemical precursor.', 'Store under lock and key. Keep away from strong oxidizers, alkalis, acids. Maintain in ventilated chemical safety storage cabinets.', 'Endogenous metabolic byproduct of amino acid demethylation, toxic in high levels, cross-links DNA and proteins causing genetic mutations.', 'Biological specimen tissue preservative (formalin), industrial adhesive resin precursor (urea-formaldehyde), industrial disinfectant.', 'C=O', 'InChI=1S/CH2O/c1-2/h1H2', 712, 'CHEBI:16842', 'Simple Aldehydes', 'Precursor to polyoxymethylene plastics, urea-formaldehyde adhesives, textile finishing resins.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "compounds" ("id", "category_id", "name", "slug", "formula", "iupac_name", "cas_number", "molecular_weight", "description", "storage_recommendations", "biological_role", "applications", "smiles", "inchi", "pubchem_cid", "chebi_id", "subcategory", "industrial_uses") VALUES (10, 16, 'Aspirin', 'aspirin', 'C9H8O4', '2-acetyloxybenzoic acid', '50-78-2', 180.158, 'Aspirin, also known as acetylsalicylic acid (ASA), is a common nonsteroidal anti-inflammatory drug (NSAID) used to reduce pain, fever, and inflammation, and as an antithrombotic agent.', 'Store at room temperature in dry containers. Keep away from moisture to prevent hydrolysis into salicylic acid.', 'Irreversible inhibitor of cyclooxygenase enzymes (COX-1 and COX-2), preventing prostaglandin and thromboxane synthesis.', 'Analgesic for pain relief, antipyretic for reducing fever, anti-inflammatory for arthritis, and low-dose antiplatelet drug for stroke prevention.', 'CC(=O)Oc1ccccc1C(=O)O', 'InChI=1S/C9H8O4/c1-5(10)13-8-4-2-3-7(8)9(11)12/h2-4H,1H3,(H,11,12)', 2244, 'CHEBI:15365', 'Salicylates', 'Pharmaceutical active ingredient synthesis and formulation tableting.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "compounds" ("id", "category_id", "name", "slug", "formula", "iupac_name", "cas_number", "molecular_weight", "description", "storage_recommendations", "biological_role", "applications", "smiles", "inchi", "pubchem_cid", "chebi_id", "subcategory", "industrial_uses") VALUES (11, 17, 'Buckminsterfullerene', 'buckminsterfullerene', 'C60', '(C60-Ih)[5,6]fullerene', '99685-96-8', 720.64, 'Buckminsterfullerene (C60), also known as the Buckyball, is a spherical carbon allotrope consisting of 60 carbon atoms structured in twenty hexagons and twelve pentagons, resembling a soccer ball.', 'Store at room temperature in dark, tightly closed vials. Keep away from strong light and oxidizing agents.', 'Potential antioxidant/radical scavenger due to high electron affinity; studied for drug delivery vector applications.', 'Superconductor compound precursor, organic photovoltaic cells electron acceptor, lubricants additive, nanotechnology research material.', 'C12=C3C4=C5C6=C1... (abbreviated C60 cage representation)', 'InChI=1S/C60/c1-2-5-6-3(1)8-12-10-4(2)9-15-18-20-17-11(5)14-23-25-22-13(6)21-24-19(7-8)27-30-28(12)32-35-33(10)34(9)41-43-38(15)37(18)46-48-40(17)39(14)47-50-42(23)45(22)52-54-44(21)49(24)51(25)55-57-53(52)56(54)59-60-58(55)57/i', 123532, 'CHEBI:33128', 'Fullerenes', 'Electron acceptors in organic solar panels, research standard for nanoscale structures, mechanical lubricant enhancers.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "compounds" ("id", "category_id", "name", "slug", "formula", "iupac_name", "cas_number", "molecular_weight", "description", "storage_recommendations", "biological_role", "applications", "smiles", "inchi", "pubchem_cid", "chebi_id", "subcategory", "industrial_uses") VALUES (12, 10, 'Lysozyme', 'lysozyme', 'C688H1053N209O193S10', 'Human Lysozyme C', '9001-63-2', 14700.2, 'Lysozyme is an enzyme that catalyzes the hydrolysis of 1,4-beta-linkages between N-acetylmuramic acid and N-acetylglucosamine residues in peptidoglycan bacterial cell walls. It is abundant in secretions like tears, saliva, and mucus.', 'Store lyophilized powder at -20 °C. Reconstituted solutions should be stored at 4 °C or aliquoted and frozen to maintain activity.', 'Innate immune defense against Gram-positive bacterial infections by lysing their cell wall peptidoglycan layer.', 'Antibacterial agent in food preservation, clinical diagnostic reagent, structural reference standard in protein crystallography.', 'N/A (Macromolecule)', 'N/A (Macromolecule)', 6914757, 'CHEBI:6687', 'Hydrolases', 'Antibacterial enzyme in winemaking and cheese production, clinical diagnostic assays.') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "compounds" ("id", "category_id", "name", "slug", "formula", "iupac_name", "cas_number", "molecular_weight", "description", "storage_recommendations", "biological_role", "applications", "smiles", "inchi", "pubchem_cid", "chebi_id", "subcategory", "industrial_uses") VALUES (13, 14, 'DNA Oligonucleotide', 'dna', '(C10H12N5O6P)n', 'Deoxyribonucleic acid oligonucleotide', '9007-49-2', 6500.0, 'Deoxyribonucleic acid (DNA) oligonucleotide is a short polymer segment of nucleotide monomers carrying genetic instructions used in growth, development, and functioning of organisms.', 'Store at -20 °C in Tris-EDTA buffer. Avoid acidic environments to prevent depurination.', 'Primary template for RNA transcription, DNA replication, and vector of inheritance.', 'Primers for Polymerase Chain Reaction (PCR), gene sequencing probes, and molecular diagnostics.', 'N/A (Polymer)', 'N/A (Polymer)', NULL, 'CHEBI:16991', 'Biopolymers', 'Diagnostic PCR kits assembly, gene synthesis templates production.') ON CONFLICT ("id") DO NOTHING;
SELECT setval(pg_get_serial_sequence('"compounds"', 'id'), COALESCE(MAX(id), 1)) FROM "compounds";

-- Table: biomolecules (3 records)
INSERT INTO "biomolecules" ("id", "compound_id", "molecule_type", "sequence", "structure_class") VALUES (1, 7, 'Nucleoside Triphosphate', 'N/A', 'Purine Nucleotide') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "biomolecules" ("id", "compound_id", "molecule_type", "sequence", "structure_class") VALUES (2, 12, 'Protein', 'KVFERCELARTLKRLGMDGYRGISLANWMCLAKWESGYNTRATNYNAGDRSTDYGIFQINSRYWCNDGKTPGAVNACHLSCSALLQDNIADAVACAKRVVRDPQGIRAWVAWRNRCQNRDVRQYVQGCGV', 'Globular Hydrolase (Alpha/Beta Protein)') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "biomolecules" ("id", "compound_id", "molecule_type", "sequence", "structure_class") VALUES (3, 13, 'DNA Oligonucleotide', '5''-CGCGAATTCGCG-3''', 'Double-stranded DNA (B-form)') ON CONFLICT ("id") DO NOTHING;
SELECT setval(pg_get_serial_sequence('"biomolecules"', 'id'), COALESCE(MAX(id), 1)) FROM "biomolecules";

-- Table: proteins (1 records)
INSERT INTO "proteins" ("id", "compound_id", "gene_name", "organism", "sequence", "pdb_id", "uniprot_id") VALUES (1, 12, 'LYZ', 'Homo sapiens (Human)', 'KVFERCELARTLKRLGMDGYRGISLANWMCLAKWESGYNTRATNYNAGDRSTDYGIFQINSRYWCNDGKTPGAVNACHLSCSALLQDNIADAVACAKRVVRDPQGIRAWVAWRNRCQNRDVRQYVQGCGV', '1A8M', 'P61626') ON CONFLICT ("id") DO NOTHING;
SELECT setval(pg_get_serial_sequence('"proteins"', 'id'), COALESCE(MAX(id), 1)) FROM "proteins";

-- Table: enzymes (1 records)
INSERT INTO "enzymes" ("id", "protein_id", "ec_number", "catalytic_activity", "substrate") VALUES (1, 1, '3.2.1.17', 'Hydrolysis of 1,4-beta-linkages between N-acetylmuramic acid and N-acetylglucosamine residues', 'Bacterial peptidoglycan cell walls') ON CONFLICT ("id") DO NOTHING;
SELECT setval(pg_get_serial_sequence('"enzymes"', 'id'), COALESCE(MAX(id), 1)) FROM "enzymes";

-- Table: physical_properties (13 records)
INSERT INTO "physical_properties" ("id", "compound_id", "melting_point", "boiling_point", "density", "solubility", "appearance") VALUES (1, 1, '0.0 °C (32.0 °F; 273.15 K)', '99.98 °C (211.96 °F; 373.13 K)', '0.9998 g/cm³ (at 0 °C) / 0.997 g/cm³ (at 25 °C)', 'Miscible in polar solvents (Universal solvent)', 'Colorless, odorless, tasteless liquid') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "physical_properties" ("id", "compound_id", "melting_point", "boiling_point", "density", "solubility", "appearance") VALUES (2, 2, '-114.14 °C (-173.45 °F; 159.01 K)', '78.24 °C (172.83 °F; 351.39 K)', '0.7893 g/cm³ (at 20 °C)', 'Miscible in water, benzene, ether, acetone, chloroform', 'Clear, colorless liquid with a pleasant, characteristic spirituous odor') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "physical_properties" ("id", "compound_id", "melting_point", "boiling_point", "density", "solubility", "appearance") VALUES (3, 3, '-97.6 °C (-143.7 °F; 175.6 K)', '64.7 °C (148.5 °F; 337.8 K)', '0.792 g/cm³ (at 20 °C)', 'Miscible in water, ethanol, ether, benzene, chloroform', 'Clear, colorless, volatile liquid with a mild alcoholic odor') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "physical_properties" ("id", "compound_id", "melting_point", "boiling_point", "density", "solubility", "appearance") VALUES (4, 4, '5.53 °C (41.95 °F; 278.68 K)', '80.1 °C (176.2 °F; 353.2 K)', '0.8765 g/cm³ (at 20 °C)', 'Slightly soluble in water (1.79 g/L at 25 °C), miscible in organic solvents', 'Clear, colorless liquid with a sweet, gasoline-like odor') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "physical_properties" ("id", "compound_id", "melting_point", "boiling_point", "density", "solubility", "appearance") VALUES (5, 5, '235 °C (455 °F) (Anhydrous)', 'Sublimes at 178 °C (352 °F)', '1.23 g/cm³ (at 18 °C)', 'Soluble in water (2.17 g/100 mL at 25 °C, 66 g/100 mL at 80 °C), chloroform, ethanol', 'White, odorless crystalline needles or powder with a bitter taste') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "physical_properties" ("id", "compound_id", "melting_point", "boiling_point", "density", "solubility", "appearance") VALUES (6, 6, '-45 °C (-49 °F; 228 K)', '88 °C (190 °F; 361 K)', '0.8814 g/cm³ (at 20 °C)', 'Soluble in water (80 g/L at 20 °C), miscible in alcohol, ether, and acetone', 'Colorless, volatile liquid with a characteristic ether-like odor') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "physical_properties" ("id", "compound_id", "melting_point", "boiling_point", "density", "solubility", "appearance") VALUES (7, 7, '187 °C (369 °F) (Decomposes)', 'N/A (Solid)', '1.04 g/cm³', 'Highly soluble in water (> 50 mg/mL at 25 °C), insoluble in organic solvents', 'White, odorless crystalline powder') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "physical_properties" ("id", "compound_id", "melting_point", "boiling_point", "density", "solubility", "appearance") VALUES (8, 8, '-94.7 °C', '56.05 °C', '0.784 g/cm³', 'Miscible in water, ethanol, diethyl ether, chloroform', 'Clear, colorless, volatile liquid with a sweet, pungent odor') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "physical_properties" ("id", "compound_id", "melting_point", "boiling_point", "density", "solubility", "appearance") VALUES (9, 9, '-92 °C', '-19 °C', '0.815 g/cm³ (at -20 °C)', 'Highly soluble in water (> 400 g/L), soluble in ethanol, diethyl ether', 'Colorless, pungent, suffocating gas (sold commercially as 37% aqueous solution, formalin)') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "physical_properties" ("id", "compound_id", "melting_point", "boiling_point", "density", "solubility", "appearance") VALUES (10, 10, '135 °C', '140 °C (Decomposes)', '1.40 g/cm³', 'Slightly soluble in water (3 mg/mL at 25 °C), soluble in ethanol, ether, chloroform', 'White, crystalline powder or monoclinic needles with a slightly acid taste') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "physical_properties" ("id", "compound_id", "melting_point", "boiling_point", "density", "solubility", "appearance") VALUES (11, 11, 'Sublimes at >280 °C (under vacuum)', 'N/A', '1.65 g/cm³', 'Insoluble in water, slightly soluble in toluene (2.8 mg/mL), benzene, carbon disulfide', 'Dark brown to black crystalline solid or fine powder') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "physical_properties" ("id", "compound_id", "melting_point", "boiling_point", "density", "solubility", "appearance") VALUES (12, 12, 'Decomposes / Denatures at >72 °C', 'N/A', '~1.35.0 g/cm³ (dry)', 'Soluble in aqueous buffers, saline, and water up to 50 mg/mL', 'White to off-white lyophilized powder') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "physical_properties" ("id", "compound_id", "melting_point", "boiling_point", "density", "solubility", "appearance") VALUES (13, 13, 'Melts/Denatures at 75-85 °C (dependent on GC content)', 'N/A', '~1.70 g/cm³', 'Highly soluble in aqueous buffers, slightly soluble in water, insoluble in ethanol', 'White, fibrous solid or aqueous solution') ON CONFLICT ("id") DO NOTHING;
SELECT setval(pg_get_serial_sequence('"physical_properties"', 'id'), COALESCE(MAX(id), 1)) FROM "physical_properties";

-- Table: chemical_properties (13 records)
INSERT INTO "chemical_properties" ("id", "compound_id", "acidity_pka", "refractive_index", "chemical_stability", "reactivity") VALUES (1, 1, '13.999 (at 25 °C)', '1.3330 (at 20 °C)', 'Highly stable, non-flammable', 'Reacts violently with alkali metals (e.g. Sodium) producing Hydrogen gas') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "chemical_properties" ("id", "compound_id", "acidity_pka", "refractive_index", "chemical_stability", "reactivity") VALUES (2, 2, '15.9', '1.361', 'Stable under recommended storage conditions, volatile', 'Reacts with strong oxidizing agents, acid chlorides, acid anhydrides, and alkali metals') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "chemical_properties" ("id", "compound_id", "acidity_pka", "refractive_index", "chemical_stability", "reactivity") VALUES (3, 3, '15.5', '1.328', 'Stable under standard conditions. Volatile and highly flammable', 'Reacts violently with strong oxidizers, acid chlorides, acid anhydrides, and alkali metals') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "chemical_properties" ("id", "compound_id", "acidity_pka", "refractive_index", "chemical_stability", "reactivity") VALUES (4, 4, '43', '1.5010 (at 20 °C)', 'Stable, highly flammable, planar aromatic ring resistant to addition reactions', 'Undergoes electrophilic aromatic substitution (nitration, halogenation, alkylation)') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "chemical_properties" ("id", "compound_id", "acidity_pka", "refractive_index", "chemical_stability", "reactivity") VALUES (5, 5, '-0.13 (conjugate acid)', 'N/A (Solid)', 'Stable under normal room temperatures, weak organic base', 'Oxidized to dimethylalloxan and methylurea with strong oxidants. Subject to electrophilic substitution at carbon-8') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "chemical_properties" ("id", "compound_id", "acidity_pka", "refractive_index", "chemical_stability", "reactivity") VALUES (6, 6, 'N/A', '1.420', 'Stable under standard conditions. May form explosive peroxides on prolonged exposure to air and light', 'Generally inert ether, but undergoes ring-cleaving reactions under highly acidic conditions') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "chemical_properties" ("id", "compound_id", "acidity_pka", "refractive_index", "chemical_stability", "reactivity") VALUES (7, 7, '0.9, 1.5, 2.1, 6.8 (Multiple acidic phosphate groups)', 'N/A', 'Unstable in aqueous solutions at high temperatures, hydrolyzes slowly to ADP at room temperature', 'Subject to nucleophilic attack on the phosphate groups, driving phosphorylation reactions') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "chemical_properties" ("id", "compound_id", "acidity_pka", "refractive_index", "chemical_stability", "reactivity") VALUES (8, 8, '24.2', '1.3588', 'Stable under normal storage conditions, highly volatile', 'Reacts with strong oxidizing agents, halogenated compounds, and reducing agents') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "chemical_properties" ("id", "compound_id", "acidity_pka", "refractive_index", "chemical_stability", "reactivity") VALUES (9, 9, '13.27', '1.37 (Formalin)', 'Highly reactive, polymerizes spontaneously to paraformaldehyde unless stabilized with methanol', 'Easily oxidized to formic acid, undergoes nucleophilic addition reactions, cross-links amines') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "chemical_properties" ("id", "compound_id", "acidity_pka", "refractive_index", "chemical_stability", "reactivity") VALUES (10, 10, '3.5', 'N/A', 'Stable in dry air, but hydrolyzes gradually in moist environments into acetic and salicylic acids', 'Undergoes transesterification, easily hydrolyzed by base, ester linkage cleaved in acids') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "chemical_properties" ("id", "compound_id", "acidity_pka", "refractive_index", "chemical_stability", "reactivity") VALUES (11, 11, 'N/A', '2.2 (Solid film)', 'Thermally stable up to 500 °C in air, highly stable cage structure', 'Electrophilic addition reactive, acts as an electron-deficient alkene, undergoes hydrogenation and halogenation') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "chemical_properties" ("id", "compound_id", "acidity_pka", "refractive_index", "chemical_stability", "reactivity") VALUES (12, 12, 'Isoelectric Point (pI) = 11.35', 'N/A', 'Stable at acidic to neutral pH. Highly susceptible to denaturing agents (urea, guanidine HCl) and high temperatures', 'Enzymatic hydrolysis of glycosidic bonds in bacterial peptidoglycan') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "chemical_properties" ("id", "compound_id", "acidity_pka", "refractive_index", "chemical_stability", "reactivity") VALUES (13, 13, '2.1 (Phosphate backbone ionization)', 'N/A', 'Highly stable under alkaline or neutral conditions. Slowly hydrolyzes in hot acidic solutions', 'Undergoes hybridization with complementary strands to form double-stranded helices') ON CONFLICT ("id") DO NOTHING;
SELECT setval(pg_get_serial_sequence('"chemical_properties"', 'id'), COALESCE(MAX(id), 1)) FROM "chemical_properties";

-- Table: hazards (13 records)
INSERT INTO "hazards" ("id", "compound_id", "ghs_classification", "hazard_statements", "precautionary_statements", "safety_equipment") VALUES (1, 1, 'Not classified as hazardous', 'None', 'None', 'Standard lab safety goggles') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "hazards" ("id", "compound_id", "ghs_classification", "hazard_statements", "precautionary_statements", "safety_equipment") VALUES (2, 2, 'Class 3 Flammable Liquid, Eye Irritant (Category 2A)', 'H225: Highly flammable liquid and vapor. H319: Causes serious eye irritation.', 'P210: Keep away from heat, hot surfaces, sparks, open flames. P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes.', 'Safety glasses, flame-retardant lab coat, nitrile gloves, chemical fume hood for vapors') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "hazards" ("id", "compound_id", "ghs_classification", "hazard_statements", "precautionary_statements", "safety_equipment") VALUES (3, 3, 'Class 3 Flammable Liquid, Acute Toxicity (Oral/Dermal/Inhalation, Category 3), target Organ Toxicity (Category 1)', 'H225: Highly flammable liquid and vapor. H301+H311+H331: Toxic if swallowed, in contact with skin, or if inhaled. H370: Causes damage to organs (optic nerve).', 'P210: Keep away from heat, sparks, open flames. P280: Wear protective gloves/clothing/eye protection. P301+P310: IF SWALLOWED: Immediately call a POISON CENTER/doctor.', 'Butol/nitrile gloves, splash goggles, flame-resistant lab coat, chemical fume hood') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "hazards" ("id", "compound_id", "ghs_classification", "hazard_statements", "precautionary_statements", "safety_equipment") VALUES (4, 4, 'Class 3 Flammable Liquid, Carcinogen (Category 1A), Mutagen (Category 1B)', 'H225: Highly flammable liquid and vapor. H350: May cause cancer. H340: May cause genetic defects.', 'P201: Obtain special instructions before use. P280: Wear protective gloves/clothing/eye protection. P308+P309: IF exposed or concerned: Get medical advice.', 'Nitrile/Viton gloves, face shield, chemical-resistant apron, explosion-proof fume hood') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "hazards" ("id", "compound_id", "ghs_classification", "hazard_statements", "precautionary_statements", "safety_equipment") VALUES (5, 5, 'Acute Toxicity (Oral, Category 4)', 'H302: Harmful if swallowed.', 'P264: Wash skin thoroughly after handling. P301+P312: IF SWALLOWED: Call a poison control center or doctor if you feel unwell.', 'Standard lab safety goggles, disposable latex/nitrile gloves') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "hazards" ("id", "compound_id", "ghs_classification", "hazard_statements", "precautionary_statements", "safety_equipment") VALUES (6, 6, 'Class 3 Flammable Liquid, Eye Irritant (Category 2A)', 'H225: Highly flammable liquid and vapor. H319: Causes serious eye irritation.', 'P210: Keep away from heat, hot surfaces, sparks, open flames. P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes.', 'Safety glasses, flame-retardant lab coat, nitrile gloves, chemical fume hood') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "hazards" ("id", "compound_id", "ghs_classification", "hazard_statements", "precautionary_statements", "safety_equipment") VALUES (7, 7, 'Not classified as hazardous', 'None', 'None', 'Standard lab safety goggles, nitrile gloves') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "hazards" ("id", "compound_id", "ghs_classification", "hazard_statements", "precautionary_statements", "safety_equipment") VALUES (8, 8, 'Class 3 Flammable Liquid, Eye Irritant (Category 2A), Target Organ Toxicity (Category 3 - Drowsiness)', 'H225: Highly flammable liquid and vapor. H319: Causes serious eye irritation. H336: May cause drowsiness or dizziness.', 'P210: Keep away from heat, sparks, open flames. P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes.', 'Safety glasses, nitrile gloves, lab coat, fume hood') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "hazards" ("id", "compound_id", "ghs_classification", "hazard_statements", "precautionary_statements", "safety_equipment") VALUES (9, 9, 'Acute Toxicity (Oral/Dermal/Inhalation, Category 3), Carcinogen (Category 1A), Skin Sensitization (Category 1)', 'H301+H311+H331: Toxic if swallowed, in contact with skin, or if inhaled. H350: May cause cancer. H317: May cause an allergic skin reaction.', 'P201: Obtain special instructions before use. P280: Wear protective gloves/clothing/eye protection. P301+P310: IF SWALLOWED: Immediately call a POISON CENTER.', 'Nitrile/neoprene gloves, splash goggles, lab coat, chemical fume hood') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "hazards" ("id", "compound_id", "ghs_classification", "hazard_statements", "precautionary_statements", "safety_equipment") VALUES (10, 10, 'Acute Toxicity (Oral, Category 4), Eye Irritant (Category 2A)', 'H302: Harmful if swallowed. H319: Causes serious eye irritation.', 'P264: Wash skin thoroughly after handling. P301+P312: IF SWALLOWED: Call a POISON CENTER if you feel unwell.', 'Safety glasses, nitrile gloves, lab coat') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "hazards" ("id", "compound_id", "ghs_classification", "hazard_statements", "precautionary_statements", "safety_equipment") VALUES (11, 11, 'Eye Irritant (Category 2B), Target Organ Toxicity (Category 3 - Respiratory)', 'H320: Causes eye irritation. H335: May cause respiratory irritation.', 'P261: Avoid breathing dust. P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes.', 'Safety glasses, nitrile gloves, dust mask or respirator, laboratory hood') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "hazards" ("id", "compound_id", "ghs_classification", "hazard_statements", "precautionary_statements", "safety_equipment") VALUES (12, 12, 'Sensitization - Respiratory (Category 1), Eye Irritant (Category 2)', 'H334: May cause allergy or asthma symptoms or breathing difficulties if inhaled. H319: Causes serious eye irritation.', 'P261: Avoid breathing dust/fume/gas/mist/vapors/spray. P342+P311: If experiencing respiratory symptoms: Call a poison center or doctor.', 'Face mask/respirator to prevent dust inhalation, nitrile gloves, lab coat, safety goggles') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "hazards" ("id", "compound_id", "ghs_classification", "hazard_statements", "precautionary_statements", "safety_equipment") VALUES (13, 13, 'Not classified as hazardous', 'None', 'None', 'Standard lab safety goggles') ON CONFLICT ("id") DO NOTHING;
SELECT setval(pg_get_serial_sequence('"hazards"', 'id'), COALESCE(MAX(id), 1)) FROM "hazards";

-- Table: references (13 records)
INSERT INTO "references" ("id", "compound_id", "citation", "doi", "url") VALUES (1, 1, 'Lide, D. R. (2004). CRC Handbook of Chemistry and Physics (85th ed.). CRC Press.', '10.1201/9781420036688', 'https://www.crcpress.com') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "references" ("id", "compound_id", "citation", "doi", "url") VALUES (2, 2, 'National Center for Biotechnology Information (2026). PubChem Compound Summary for CID 702, Ethanol.', '10.1093/pubchem/702', 'https://pubchem.ncbi.nlm.nih.gov/compound/Ethanol') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "references" ("id", "compound_id", "citation", "doi", "url") VALUES (3, 3, 'National Center for Biotechnology Information (2026). PubChem Compound Summary for CID 887, Methanol.', '10.1093/pubchem/887', 'https://pubchem.ncbi.nlm.nih.gov/compound/Methanol') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "references" ("id", "compound_id", "citation", "doi", "url") VALUES (4, 4, 'IARC Working Group on the Evaluation of Carcinogenic Risks to Humans. (2018). Benzene. IARC Monographs, Volume 120.', '10.2307/iarc.benzene.120', 'https://monographs.iarc.who.int') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "references" ("id", "compound_id", "citation", "doi", "url") VALUES (5, 5, 'Nehlig, A., Daval, J. L., & Debry, G. (1992). Caffeine and the central nervous system: brain action. Brain Research Reviews, 17(2), 139-170.', '10.1016/0169-328X(92)90012-B', 'https://www.sciencedirect.com') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "references" ("id", "compound_id", "citation", "doi", "url") VALUES (6, 6, 'National Center for Biotechnology Information (2026). PubChem Compound Summary for CID 8882, Tetrahydropyran.', '10.1093/pubchem/8882', 'https://pubchem.ncbi.nlm.nih.gov/compound/Tetrahydropyran') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "references" ("id", "compound_id", "citation", "doi", "url") VALUES (7, 7, 'Nelson, D. L., & Cox, M. M. (2017). Lehninger Principles of Biochemistry (7th ed.). W. H. Freeman.', '10.2307/biochem.lehninger.7', 'https://macmillanlearning.com') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "references" ("id", "compound_id", "citation", "doi", "url") VALUES (8, 8, 'National Center for Biotechnology Information (2026). PubChem Compound Summary for CID 180, Acetone.', '10.1093/pubchem/180', 'https://pubchem.ncbi.nlm.nih.gov/compound/Acetone') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "references" ("id", "compound_id", "citation", "doi", "url") VALUES (9, 9, 'IARC Working Group on the Evaluation of Carcinogenic Risks to Humans. (2006). Formaldehyde. IARC Monographs, Volume 88.', '10.2307/iarc.formal.88', 'https://monographs.iarc.who.int') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "references" ("id", "compound_id", "citation", "doi", "url") VALUES (10, 10, 'Vane, J. R. (1971). Inhibition of prostaglandin synthesis as a mechanism of action for aspirin-like drugs. Nature New Biology, 231(25), 232-235.', '10.1038/newbio231232a0', 'https://www.nature.com') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "references" ("id", "compound_id", "citation", "doi", "url") VALUES (11, 11, 'Kroto, H. W., Heath, J. R., O''Brien, S. C., Curl, R. F., & Smalley, R. E. (1985). C60: Buckminsterfullerene. Nature, 318(6042), 162-163.', '10.1038/318162a0', 'https://www.nature.com/articles/318162a0') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "references" ("id", "compound_id", "citation", "doi", "url") VALUES (12, 12, 'Blake, C. C. F., Koenig, D. F., Mair, G. A., North, A. C. T., Phillips, D. C., & Sarma, V. R. (1965). Structure of Hen Egg-White Lysozyme. Nature, 206(4986), 757-761.', '10.1038/206757a0', 'https://www.nature.com/articles/206757a0') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "references" ("id", "compound_id", "citation", "doi", "url") VALUES (13, 13, 'Watson, J. D., & Crick, F. H. (1953). Molecular structure of nucleic acids: a structure for deoxyribose nucleic acid. Nature, 171(4356), 737-738.', '10.1038/171737a0', 'https://www.nature.com/articles/171737a0') ON CONFLICT ("id") DO NOTHING;
SELECT setval(pg_get_serial_sequence('"references"', 'id'), COALESCE(MAX(id), 1)) FROM "references";

-- Table: visualization_metadata (13 records)
INSERT INTO "visualization_metadata" ("id", "compound_id", "two_d_svg", "three_d_sdf", "three_d_model_type") VALUES (1, 1, '<svg viewBox="0 0 100 60" width="100" height="60" xmlns="http://www.w3.org/2000/svg"><line x1="20" y1="40" x2="50" y2="20" stroke="black" stroke-width="2"/><line x1="80" y1="40" x2="50" y2="20" stroke="black" stroke-width="2"/><circle cx="50" cy="20" r="12" fill="white" stroke="black" stroke-width="2"/><text x="45" y="25" font-family="monospace" font-weight="bold" font-size="14">O</text><circle cx="20" cy="40" r="10" fill="white" stroke="black" stroke-width="2"/><text x="15" y="45" font-family="monospace" font-size="12">H</text><circle cx="80" cy="40" r="10" fill="white" stroke="black" stroke-width="2"/><text x="75" y="45" font-family="monospace" font-size="12">H</text></svg>', 'Water
  3Dmol.js

  3  2  0  0  0  0  0  0  0  0999 V2000
    0.0000    0.0000    0.0658 O   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000    0.7570   -0.5201 H   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000   -0.7570   -0.5201 H   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0  0  0  0
  1  3  1  0  0  0  0
M  END
', 'sdf') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "visualization_metadata" ("id", "compound_id", "two_d_svg", "three_d_sdf", "three_d_model_type") VALUES (2, 2, '<svg viewBox="0 0 160 60" width="160" height="60" xmlns="http://www.w3.org/2000/svg"><line x1="30" y1="30" x2="80" y2="30" stroke="black" stroke-width="2"/><line x1="80" y1="30" x2="130" y2="30" stroke="black" stroke-width="2"/><circle cx="30" cy="30" r="12" fill="white" stroke="black" stroke-width="2"/><text x="23" y="35" font-family="monospace" font-size="14">CH3</text><circle cx="80" cy="30" r="12" fill="white" stroke="black" stroke-width="2"/><text x="73" y="35" font-family="monospace" font-size="14">CH2</text><circle cx="130" cy="30" r="12" fill="white" stroke="black" stroke-width="2"/><text x="123" y="35" font-family="monospace" font-size="14">OH</text></svg>', 'Ethanol
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
', 'sdf') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "visualization_metadata" ("id", "compound_id", "two_d_svg", "three_d_sdf", "three_d_model_type") VALUES (3, 3, '<svg viewBox="0 0 100 60" width="100" height="60" xmlns="http://www.w3.org/2000/svg"><line x1="25" y1="30" x2="75" y2="30" stroke="black" stroke-width="2"/><circle cx="25" cy="30" r="12" fill="white" stroke="black" stroke-width="2"/><text x="18" y="35" font-family="monospace" font-size="12">CH3</text><circle cx="75" cy="30" r="12" fill="white" stroke="black" stroke-width="2"/><text x="68" y="35" font-family="monospace" font-size="12">OH</text></svg>', 'Methanol
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
', 'sdf') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "visualization_metadata" ("id", "compound_id", "two_d_svg", "three_d_sdf", "three_d_model_type") VALUES (4, 4, '<svg viewBox="0 0 100 100" width="100" height="100" xmlns="http://www.w3.org/2000/svg"><polygon points="50,15 80,32 80,68 50,85 20,68 20,32" stroke="black" stroke-dasharray="none" stroke-width="2" fill="none"/><circle cx="50" cy="50" r="22" stroke="black" stroke-dasharray="4,4" stroke-width="2" fill="none"/></svg>', 'Benzene
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
', 'sdf') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "visualization_metadata" ("id", "compound_id", "two_d_svg", "three_d_sdf", "three_d_model_type") VALUES (5, 5, '<svg viewBox="0 0 120 100" width="120" height="100" xmlns="http://www.w3.org/2000/svg"><polygon points="30,30 65,30 80,50 65,70 30,70 15,50" stroke="black" stroke-width="2" fill="none"/><polygon points="65,30 95,15 110,40 90,60 65,50" stroke="black" stroke-width="2" fill="none"/></svg>', 'Caffeine
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
', 'sdf') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "visualization_metadata" ("id", "compound_id", "two_d_svg", "three_d_sdf", "three_d_model_type") VALUES (6, 6, '<svg viewBox="0 0 100 100" width="100" height="100" xmlns="http://www.w3.org/2000/svg"><path d="M 50,15 L 80,32 L 80,50 M 80,62 L 80,68 L 50,85 L 20,68 L 20,32 L 50,15" stroke="black" stroke-width="2" fill="none" stroke-linejoin="round"/><text x="75" y="60" font-family="sans-serif" font-weight="bold" font-size="12" fill="black">O</text></svg>', 'Tetrahydropyran
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
', 'sdf') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "visualization_metadata" ("id", "compound_id", "two_d_svg", "three_d_sdf", "three_d_model_type") VALUES (7, 7, '<svg viewBox="0 0 160 100" width="160" height="100" xmlns="http://www.w3.org/2000/svg"><polygon points="20,40 45,25 70,40 58,65 32,65" stroke="black" stroke-width="2" fill="none"/><rect x="75" y="30" width="20" height="20" stroke="black" stroke-width="2" fill="none"/><circle cx="110" cy="40" r="8" stroke="black" stroke-width="2" fill="none"/><text x="108" y="44" font-family="sans-serif" font-size="10">P</text><circle cx="130" cy="40" r="8" stroke="black" stroke-width="2" fill="none"/><text x="128" y="44" font-family="sans-serif" font-size="10">P</text><circle cx="150" cy="40" r="8" stroke="black" stroke-width="2" fill="none"/><text x="148" y="44" font-family="sans-serif" font-size="10">P</text><text x="35" y="50" font-family="sans-serif" font-size="10">Ribose</text><text x="78" y="44" font-family="sans-serif" font-size="10">Ade</text></svg>', 'ATP
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
', 'sdf') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "visualization_metadata" ("id", "compound_id", "two_d_svg", "three_d_sdf", "three_d_model_type") VALUES (8, 8, '<svg viewBox="0 0 100 60" width="100" height="60" xmlns="http://www.w3.org/2000/svg"><line x1="20" y1="40" x2="50" y2="25" stroke="black" stroke-width="2"/><line x1="80" y1="40" x2="50" y2="25" stroke="black" stroke-width="2"/><line x1="48" y1="25" x2="48" y2="5" stroke="black" stroke-width="2"/><line x1="52" y1="25" x2="52" y2="5" stroke="black" stroke-width="2"/><circle cx="50" cy="25" r="10" fill="white" stroke="black" stroke-width="2"/><text x="45" y="30" font-family="monospace" font-size="12">C</text><text x="12" y="45" font-family="monospace" font-size="10">CH3</text><text x="75" y="45" font-family="monospace" font-size="10">CH3</text><text x="47" y="2" font-family="monospace" font-weight="bold" font-size="12">O</text></svg>', 'Acetone
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
', 'sdf') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "visualization_metadata" ("id", "compound_id", "two_d_svg", "three_d_sdf", "three_d_model_type") VALUES (9, 9, '<svg viewBox="0 0 100 60" width="100" height="60" xmlns="http://www.w3.org/2000/svg"><line x1="50" y1="40" x2="50" y2="15" stroke="black" stroke-width="2"/><line x1="48" y1="40" x2="48" y2="15" stroke="black" stroke-width="2"/><line x1="52" y1="40" x2="52" y2="15" stroke="black" stroke-width="2"/><circle cx="50" cy="40" r="10" fill="white" stroke="black" stroke-width="2"/><text x="45" y="45" font-family="monospace" font-size="12">CH2</text><text x="47" y="12" font-family="monospace" font-weight="bold" font-size="12">O</text></svg>', 'Formaldehyde
  3Dmol.js

  2  1  0  0  0  0  0  0  0  0999 V2000
    0.0000    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000    1.2000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  2  0  0  0  0
M  END
', 'sdf') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "visualization_metadata" ("id", "compound_id", "two_d_svg", "three_d_sdf", "three_d_model_type") VALUES (10, 10, '<svg viewBox="0 0 100 100" width="100" height="100" xmlns="http://www.w3.org/2000/svg"><polygon points="50,30 75,42 75,70 50,82 25,70 25,42" stroke="black" stroke-width="2" fill="none"/><line x1="75" y1="42" x2="90" y2="30" stroke="black" stroke-width="2"/><text x="92" y="32" font-family="sans-serif" font-size="10">O-Ac</text></svg>', 'Aspirin
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
', 'sdf') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "visualization_metadata" ("id", "compound_id", "two_d_svg", "three_d_sdf", "three_d_model_type") VALUES (11, 11, '<svg viewBox="0 0 100 100" width="100" height="100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="30" stroke="black" stroke-width="2" fill="none"/><polygon points="50,20 65,30 65,50 50,60 35,50 35,30" stroke="black" stroke-width="1" fill="none"/></svg>', 'C60
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
', 'sdf') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "visualization_metadata" ("id", "compound_id", "two_d_svg", "three_d_sdf", "three_d_model_type") VALUES (12, 12, '<svg viewBox="0 0 100 100" width="100" height="100" xmlns="http://www.w3.org/2000/svg"><path d="M20,50 Q40,20 50,50 T80,50" fill="none" stroke="black" stroke-width="3"/><circle cx="20" cy="50" r="5" fill="black"/><circle cx="50" cy="50" r="5" fill="black"/><circle cx="80" cy="50" r="5" fill="black"/></svg>', 'HEADER    HYDROLASE(O-GLYCOSYL)                   13-MAY-98   1A8M
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
', 'pdb') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "visualization_metadata" ("id", "compound_id", "two_d_svg", "three_d_sdf", "three_d_model_type") VALUES (13, 13, '<svg viewBox="0 0 100 100" width="100" height="100" xmlns="http://www.w3.org/2000/svg"><path d="M20,10 C20,90 80,10 80,90 M20,25 L80,25 M20,45 L80,45 M20,65 L80,65" stroke="black" stroke-width="2" fill="none"/></svg>', 'HEADER    DNA DOUBLE HELIX                        15-FEB-81   1BNA
TITLE     DNA 10-MER BACKBONE
ATOM      1  P   DA  A   1      -1.745   9.897  -4.135  1.00 20.00           P
ATOM      2  OP1 DA  A   1      -2.548  10.320  -5.321  1.00 20.00           O
ATOM      3  OP2 DA  A   1      -1.921   8.541  -3.521  1.00 20.00           O
ATOM      4  O5'' DA  A   1      -0.201  10.012  -4.521  1.00 20.00           O
ATOM      5  C5'' DA  A   1       0.820   9.814  -3.524  1.00 20.00           C
ATOM      6  C4'' DA  A   1       2.124  10.150  -4.215  1.00 20.00           C
ATOM      7  C3'' DA  A   1       2.254   9.412  -5.501  1.00 20.00           C
ATOM      8  O3'' DA  A   1       1.240   9.852  -6.381  1.00 20.00           O
ATOM      9  P   DT  A   2       1.450   9.642  -7.954  1.00 20.00           P
ATOM     10  OP1 DT  A   2       0.120   9.921  -8.541  1.00 20.00           O
ATOM     11  OP2 DT  A   2       2.541  10.450  -8.320  1.00 20.00           O
ATOM     12  O5'' DT  A   2       1.854   8.120  -8.154  1.00 20.00           O
ATOM     13  C5'' DT  A   2       2.852   7.641  -9.041  1.00 20.00           C
ATOM     14  C4'' DT  A   2       3.120   6.150  -8.751  1.00 20.00           C
ATOM     15  C3'' DT  A   2       1.841   5.421  -9.120  1.00 20.00           C
ATOM     16  O3'' DT  A   2       2.045   4.012  -9.001  1.00 20.00           O
TER      17      DT  A   2
END
', 'pdb') ON CONFLICT ("id") DO NOTHING;
SELECT setval(pg_get_serial_sequence('"visualization_metadata"', 'id'), COALESCE(MAX(id), 1)) FROM "visualization_metadata";

-- Table: synonyms (63 records)
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (1, 1, 'Dihydrogen monoxide') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (2, 1, 'Oxidane') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (3, 1, 'Aqua') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (4, 1, 'H2O') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (5, 1, 'Distilled water') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (6, 2, 'Ethyl alcohol') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (7, 2, 'Methylcarbinol') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (8, 2, 'Grain alcohol') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (9, 2, 'EtOH') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (10, 2, 'Drinking alcohol') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (11, 3, 'Methyl alcohol') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (12, 3, 'Wood alcohol') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (13, 3, 'Carbinol') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (14, 3, 'MeOH') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (15, 3, 'Wood spirit') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (16, 4, 'Benzol') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (17, 4, 'Cyclohexatriene') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (18, 4, 'Phene') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (19, 4, '[6]-Annulene') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (20, 4, 'Coal naphtha') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (21, 5, '1,3,7-Trimethylxanthine') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (22, 5, 'Guaranine') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (23, 5, 'Theine') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (24, 5, 'Methyltheobromine') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (25, 5, 'Caffeine anhydrous') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (26, 6, 'Oxane') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (27, 6, 'Pentamethylene oxide') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (28, 6, 'THP') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (29, 6, 'Tetrahydro-2H-pyran') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (30, 7, 'Adenosine 5''-triphosphate') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (31, 7, 'Triphosphoadenosine') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (32, 7, 'Adenylpyrophosphate') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (33, 7, 'ATP') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (34, 7, 'Striadyne') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (35, 8, '2-Propanone') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (36, 8, 'Dimethyl ketone') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (37, 8, 'Propanone') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (38, 8, 'Pyroacetic ether') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (39, 8, 'β-ketopropane') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (40, 9, 'Methanal') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (41, 9, 'Formalin') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (42, 9, 'Formic aldehyde') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (43, 9, 'Methylene oxide') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (44, 9, 'Oxomethane') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (45, 10, 'Acetylsalicylic acid') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (46, 10, 'ASA') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (47, 10, '2-Acetoxybenzoic acid') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (48, 10, 'Aspirine') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (49, 10, 'Ecotrin') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (50, 11, 'Buckyball') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (51, 11, 'Fullerene C60') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (52, 11, '[60]Fullerene') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (53, 11, 'Footballene') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (54, 11, 'Buckminster fullerene') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (55, 12, 'Muramidase') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (56, 12, 'Lytic enzyme') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (57, 12, 'Lysozyme C') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (58, 12, 'Globulin G1') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (59, 12, 'Human lysozyme') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (60, 13, 'DNA backbone') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (61, 13, 'Double helix oligonucleotide') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (62, 13, 'Deoxyribose nucleic acid segment') ON CONFLICT ("id") DO NOTHING;
INSERT INTO "synonyms" ("id", "compound_id", "synonym") VALUES (63, 13, 'PCR Primer DNA') ON CONFLICT ("id") DO NOTHING;
SELECT setval(pg_get_serial_sequence('"synonyms"', 'id'), COALESCE(MAX(id), 1)) FROM "synonyms";

