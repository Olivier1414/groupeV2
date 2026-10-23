import tempfile, unittest
from pathlib import Path
from src.core import DocumentEngine, read_rows, OUTPUT

class TestAtelier(unittest.TestCase):
    def test_read_csv(self):
        rows=read_rows(Path(__file__).resolve().parent/"data"/"exemple.csv")
        self.assertGreater(len(rows),0)
    def test_template(self):
        engine=DocumentEngine()
        text=engine.render("Attestation",{"civilite":"M.","nom":"TEST","prenom":"Jean","date":"01/01/2026","motif":"Essai","montant":"0","note":"15","email":"","numero":"AT-2026-0001"})
        self.assertIn("Jean TEST",text)
    def test_generate_both(self):
        engine=DocumentEngine()
        with tempfile.TemporaryDirectory() as tmp:
            # Teste directement les générateurs sans modifier les compteurs de production.
            from src.core import DocumentEngine as E
            from pathlib import Path
            text="TEST\nContenu de test"
            pdf=Path(tmp)/"test.pdf"; docx=Path(tmp)/"test.docx"
            E._pdf(text,pdf); E._word(text,docx)
            self.assertGreater(pdf.stat().st_size,0)
            self.assertGreater(docx.stat().st_size,0)

if __name__=="__main__":
    unittest.main(verbosity=2)
