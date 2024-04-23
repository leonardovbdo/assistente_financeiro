import unittest
from virtual_assistant import *

CHAMANDO_ASSISTENTE = r"audios\chamando assistente.wav"
CHAMANDO_JARVIS = r"audios\chamando jarvis.wav"
DEFINIR_ORCAMENTO = r"audios\definir orcamento.wav"
REGISTRAR_DESPESA = r"audios\registrar despesa.wav"
VERIFICAR_SALDO = r"audios\verificar saldo.wav"
VISUALIZAR_RELATORIO = r"audios\visualizar relatorio.wav"

class TesteNomeAssistente(unittest.TestCase):
    
    def setUp(self):
        self.deployed, self.recognizer, _, self.assistant_name, _ = initiate()

    def recognize_assistant_name_01(self):
        is_written, transcription = process_test_audio(CHAMANDO_ASSISTENTE, self.recognizer)

        self.assertTrue(is_written)

        tokens = get_tokens(transcription)
        self.assertIsNotNone(tokens)
        self.assertEqual(tokens[0], self.assistant_name)

    def not_recognize_assistant_name_02(self):
        is_written, transcription = process_test_audio(CHAMANDO_JARVIS, self.recognizer)

        self.assertTrue(is_written)

        tokens = get_tokens(transcription)
        self.assertIsNotNone(tokens)
        self.assertNotEqual(tokens[0], self.assistant_name)

class TesteFinanceiro(unittest.TestCase):

    def setUp(self):
        self.deployed, self.recognizer, self.stopping_words, self.assistant_name, self.actions = initiate()

    def testar_definir_orcamento_01(self):
        is_written, transcription = process_test_audio(DEFINIR_ORCAMENTO, self.recognizer)

        self.assertTrue(is_written)

        tokens = get_tokens(transcription)
        self.assertIsNotNone(tokens)

        tokens = remove_stopping_words(tokens, self.stopping_words)
        valido, _, _ = validate_command(tokens, self.assistant_name, self.actions)
        self.assertTrue(valido)

    def testar_registrar_despesa_02(self):
        is_written, transcription = process_test_audio(REGISTRAR_DESPESA, self.recognizer)

        self.assertTrue(is_written)

        tokens = get_tokens(transcription)
        self.assertIsNotNone(tokens)

        tokens = remove_stopping_words(tokens, self.stopping_words)
        valido, _, _ = validate_command(tokens, self.assistant_name, self.actions)
        self.assertTrue(valido)

    def testar_verificar_saldo_03(self):
        is_written, transcription = process_test_audio(VERIFICAR_SALDO, self.recognizer)

        self.assertTrue(is_written)

        tokens = get_tokens(transcription)
        self.assertIsNotNone(tokens)

        tokens = remove_stopping_words(tokens, self.stopping_words)
        valido, _, _ = validate_command(tokens, self.assistant_name, self.actions)
        self.assertTrue(valido)

    def testar_visualizar_relatorio_04(self):
        is_written, transcription = process_test_audio(VISUALIZAR_RELATORIO, self.recognizer)

        self.assertTrue(is_written)

        tokens = get_tokens(transcription)
        self.assertIsNotNone(tokens)

        tokens = remove_stopping_words(tokens, self.stopping_words)
        valido, _, _ = validate_command(tokens, self.assistant_name, self.actions)
        self.assertTrue(valido)


if __name__ == "__main__":
    carregador = unittest.TestLoader()
    testes = unittest.TestSuite()

    testes.addTest(carregador.loadTestsFromTestCase(TesteNomeAssistente))
    testes.addTest(carregador.loadTestsFromTestCase(TesteFinanceiro))

    executor = unittest.TextTestRunner()
    executor.run(testes)
