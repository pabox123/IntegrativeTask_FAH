import unittest
from normalization.canonical import SkillNormalizerPipeline, canonicalize_extracted_data


class TestNormalizationPipeline(unittest.TestCase):

    def setUp(self):
        self.pipeline = SkillNormalizerPipeline()

    def test_programming_languages_fst(self):
        self.assertEqual(self.pipeline.normalize_single_token("JS"), "JAVASCRIPT")
        self.assertEqual(self.pipeline.normalize_single_token("javascript"), "JAVASCRIPT")
        self.assertEqual(self.pipeline.normalize_single_token("py"), "PYTHON")
        self.assertEqual(self.pipeline.normalize_single_token("Python"), "PYTHON")
        self.assertEqual(self.pipeline.normalize_single_token("c++"), "CPP")

    def test_frameworks_fst(self):
        self.assertEqual(self.pipeline.normalize_single_token("React.js"), "REACT")
        self.assertEqual(self.pipeline.normalize_single_token("NodeJS"), "NODE_JS")
        self.assertEqual(self.pipeline.normalize_single_token("Django"), "DJANGO")
        self.assertEqual(self.pipeline.normalize_single_token("Spring Boot"), "SPRING_BOOT")

    def test_databases_fst(self):
        self.assertEqual(self.pipeline.normalize_single_token("Postgres"), "POSTGRESQL")
        self.assertEqual(self.pipeline.normalize_single_token("mysql"), "MYSQL")
        self.assertEqual(self.pipeline.normalize_single_token("MongoDB"), "MONGODB")

    def test_aiml_fst(self):
        self.assertEqual(self.pipeline.normalize_single_token("sklearn"), "SCIKIT_LEARN")
        self.assertEqual(self.pipeline.normalize_single_token("tf"), "TENSORFLOW")
        self.assertEqual(self.pipeline.normalize_single_token("PyTorch"), "PYTORCH")

    def test_devops_fst(self):
        self.assertEqual(self.pipeline.normalize_single_token("Git"), "GIT")
        self.assertEqual(self.pipeline.normalize_single_token("k8s"), "KUBERNETES")
        self.assertEqual(self.pipeline.normalize_single_token("Docker"), "DOCKER")

    def test_canonical_sorting_hierarchy(self):
        raw_skills = ["Docker", "NodeJS", "JS", "Postgres", "py"]
        expected_order = ["JAVASCRIPT", "PYTHON", "NODE_JS", "POSTGRESQL", "DOCKER"]

        result = self.pipeline.normalize_and_sort_skills(raw_skills)
        self.assertEqual(result, expected_order)

    def test_extracted_dict_interface(self):
        extracted_mock = {
            "programming_languages": ["JS", "py"],
            "frameworks": ["React.js"],
            "databases": ["Postgres"]
        }
        expected = ["JAVASCRIPT", "PYTHON", "REACT", "POSTGRESQL"]
        result = canonicalize_extracted_data(extracted_mock)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()