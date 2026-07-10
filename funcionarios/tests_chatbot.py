from django.test import TestCase
from funcionarios.chatbot.normalization import normalize_text
from funcionarios.chatbot.synonyms import replace_synonyms
from funcionarios.chatbot.fuzzy import levenshtein_distance, correct_sentence_words
from funcionarios.chatbot.intent import detect_intent
from funcionarios.chatbot.entities import extract_entities
from funcionarios.chatbot.engine import process_message
from funcionarios.models import Funcionario

class ChatbotNLPTests(TestCase):

    def setUp(self):
        # Cadastrar alguns funcionários para teste
        Funcionario.objects.create(
            nome="João Silva",
            cpf="111.111.111-11",
            telefone="(11) 91111-1111",
            email="joao@empresa.com",
            data_nascimento="1990-01-01",
            departamento="ti",
            cargo="Desenvolvedor",
            escolaridade="superior",
            tipo_contrato="clt",
            modelo_trabalho="remoto",
            salario=8500.00,
            data_admissao="2023-05-15",
            cidade="São Paulo",
            ativo=True
        )
        Funcionario.objects.create(
            nome="Maria Oliveira",
            cpf="222.222.222-22",
            telefone="(11) 92222-2222",
            email="maria@empresa.com",
            data_nascimento="1985-05-10",
            departamento="rh",
            cargo="Gerente",
            escolaridade="pos",
            tipo_contrato="clt",
            modelo_trabalho="presencial",
            salario=12000.00,
            data_admissao="2020-03-01",
            cidade="Rio de Janeiro",
            ativo=True
        )

    def test_normalization(self):
        self.assertEqual(normalize_text("Olá, tudo bem?"), "ola tudo bem")
        self.assertEqual(normalize_text("  Espaços   múltiplos  "), "espacos multiplos")
        self.assertEqual(normalize_text("Atenção à pontuação!!!"), "atencao a pontuacao")

    def test_synonyms(self):
        self.assertEqual(replace_synonyms("quem trabalha no recursos humanos"), "quem trabalha no rh")
        self.assertEqual(replace_synonyms("exibir colaboradores de tecnologia"), "listar funcionarios de ti")
        self.assertEqual(replace_synonyms("qual a remuneracao de joao"), "qual a salario de joao")

    def test_levenshtein(self):
        self.assertEqual(levenshtein_distance("funcionaro", "funcionario"), 1)
        self.assertEqual(levenshtein_distance("salaro", "salario"), 1)
        
        # Testar correção por palavra
        targets = ["funcionario", "salario"]
        self.assertEqual(correct_sentence_words("qual o salaro do funcionaro", targets), "qual o salario do funcionario")

    def test_intent_detection(self):
        self.assertEqual(detect_intent("media salarial"), "media_salarial")
        self.assertEqual(detect_intent("qual maior salario"), "maior_salario")
        self.assertEqual(detect_intent("quantos funcionarios existem"), "contar_funcionarios")

    def test_entity_extraction(self):
        # Buscar por João Silva
        entities = extract_entities("mostre os dados de joao silva")
        self.assertEqual(entities["name"], "João Silva")

        # Buscar por setor TI
        entities_dept = extract_entities("quem trabalha no setor de tecnologia da informacao")
        self.assertEqual(entities_dept["department"], "ti")

        # Buscar por salários > 8000
        entities_sal = extract_entities("quem recebe mais de 8000")
        self.assertEqual(entities_sal["salary_value"], 8000.0)
        self.assertEqual(entities_sal["salary_operator"], "greater")

    def test_full_pipeline(self):
        # Teste completo
        response = process_message("Quantos funcionarios existem?")
        self.assertIn("2", response)

        # Teste com erro de digitação
        response_typo = process_message("Qual o salaro medio?")
        self.assertIn("10.250", response_typo)  # (8500 + 12000) / 2 = 10250
