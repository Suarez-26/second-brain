"""Pruebas del pipeline sobre un vault temporal con su propio git (no toca el vault real).

    python -m unittest discover -s automation/tests -v
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

AUTOMATION = Path(__file__).resolve().parent.parent
TMP = Path(tempfile.mkdtemp(prefix="vault_test_"))
SECRETO = "secreto-de-prueba"
ADMIN = "573000000999"
TERCERO = "573000000001"

# El entorno se fija antes de importar los módulos: todos leen RAIZ y rutas al cargar
os.environ.update({
    "VAULT_RAIZ": str(TMP),
    "VAULT_STATE_DB": str(TMP / "state.db"),
    "VAULT_INDEX_DB": str(TMP / "index.db"),
    "ADMIN_PHONE_NUMBER": ADMIN,
    "KAPSO_WEBHOOK_SECRET": SECRETO,
    "WHATSAPP_VERIFY_TOKEN": "token-verificacion",
    "WHATSAPP_PHONE_NUMBER_ID": "111",
    "GEMINI_API_KEY": "",
})
os.environ.pop("KAPSO_WEBHOOK_INSECURE", None)
sys.path.insert(0, str(AUTOMATION))

(TMP / "meta").mkdir()
(TMP / "areas").mkdir()
(TMP / "meta" / "log.md").write_text("---\nfecha: 2026-10-01\n---\n\n# Log\n", encoding="utf-8")
(TMP / "meta" / "open-loops.md").write_text(textwrap.dedent("""\
    ---
    fecha: 2026-10-01
    ---

    # Pendientes abiertos

    - [ ] Enviar la propuesta formal a la alcaldía
    - [ ] Pedir a Diego sus enlaces oficiales

    ## Cerrados
    """), encoding="utf-8")
(TMP / "areas" / "campuslands.md").write_text(
    "---\nfecha: 2026-10-01\ncontexto: campuslands\n---\n\n# Campuslands\n\n## Sedes\nZona Franca en Floridablanca.\n",
    encoding="utf-8",
)
(TMP / "inbox").mkdir()
(TMP / "inbox" / "crudo.md").write_text("# Crudo\n\nFloridablanca mencionada en corpus crudo.\n", encoding="utf-8")
subprocess.run(["git", "init", "-q"], cwd=TMP, check=True)
subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "add", "-A"], cwd=TMP, check=True)
subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "base"], cwd=TMP, check=True)
os.environ.update({"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})

import cola  # noqa: E402
import indice  # noqa: E402
import pendientes  # noqa: E402
import vault_io  # noqa: E402


class TestVaultIO(unittest.TestCase):
    def test_escritura_concurrente_entre_procesos_no_pierde_lineas(self):
        script = (
            "import sys; sys.path.insert(0, sys.argv[1]); import vault_io\n"
            "for i in range(40): vault_io.anexar('journal/concurrente.md', f'{sys.argv[2]}-{i}\\n', 'test')\n"
        )
        env = {**os.environ, "VAULT_AUTO_COMMIT": "0"}
        procs = [subprocess.Popen([sys.executable, "-c", script, str(AUTOMATION), n], env=env) for n in ("a", "b", "c")]
        for p in procs:
            self.assertEqual(p.wait(60), 0)
        lineas = (TMP / "journal" / "concurrente.md").read_text(encoding="utf-8").split()
        self.assertEqual(len(lineas), 120)
        self.assertEqual(len(set(lineas)), 120)

    def test_capa1_y_rutas_externas_bloqueadas(self):
        with self.assertRaises(vault_io.ErrorVault):
            vault_io.anexar("meta/open-loops.md", "- [ ] colado\n", "test")
        with self.assertRaises(vault_io.ErrorVault):
            vault_io.anexar("../fuera.md", "x", "test", aprobado=True)

    def test_lote_hace_un_solo_commit(self):
        antes = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=TMP, capture_output=True, text=True).stdout
        with vault_io.lote("lote de prueba"):
            vault_io.anexar("journal/lote.md", "uno\n", "test")
            vault_io.anexar("journal/lote.md", "dos\n", "test")
        despues = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=TMP, capture_output=True, text=True).stdout
        self.assertEqual(int(despues), int(antes) + 1)
        ultimo = subprocess.run(["git", "log", "-1", "--format=%s"], cwd=TMP, capture_output=True, text=True).stdout
        self.assertIn("lote de prueba", ultimo)


class TestPendientes(unittest.TestCase):
    def setUp(self):
        vault_io.escribir(pendientes.OPEN_LOOPS, pendientes.asignar_ids, "ids", aprobado=True)

    def test_ids_idempotentes(self):
        texto = (TMP / "meta" / "open-loops.md").read_text(encoding="utf-8")
        self.assertEqual(pendientes.asignar_ids(texto), texto)
        self.assertIn("[OL-001]", texto)

    def test_el_llm_solo_propone_y_nada_cambia_sin_aprobar(self):
        antes = (TMP / "meta" / "open-loops.md").read_text(encoding="utf-8")
        ids = pendientes.proponer_desde_analisis(
            {"compromisos_nuevos": ["Llamar a Fedesoft"], "tareas_completadas": ["envié la propuesta formal a la alcaldía"]},
            origen="test",
        )
        self.assertEqual(len(ids), 2)
        self.assertEqual((TMP / "meta" / "open-loops.md").read_text(encoding="utf-8"), antes)

        for pid in ids:
            pendientes.aplicar(pid)
        despues = (TMP / "meta" / "open-loops.md").read_text(encoding="utf-8")
        self.assertIn("Llamar a Fedesoft", despues)
        self.assertRegex(despues, r"- \[x\] \[OL-\d+\] ~~Enviar la propuesta formal")
        self.assertLess(despues.index("Llamar a Fedesoft"), despues.index("## Cerrados"))
        self.assertIn("- [ ] [OL-002] Pedir a Diego", despues)

    def test_coincidencia_debil_no_propone_cierre(self):
        self.assertIsNone(pendientes.candidato_para("hablé con Diego"))


class TestCola(unittest.TestCase):
    def test_deduplicacion_y_reintentos(self):
        self.assertTrue(cola.encolar("m-dup", "test", {"x": 1}))
        self.assertFalse(cola.encolar("m-dup", "test", {"x": 1}))
        fila = cola.tomar_siguiente()
        self.assertEqual(fila["id"], "m-dup")
        cola.marcar_fallido("m-dup", "boom")
        self.assertIsNone(cola.tomar_siguiente())  # espera el backoff antes de reintentar
        cola.marcar_hecho("m-dup")


class TestIndice(unittest.TestCase):
    def test_busca_sin_acentos_y_excluye_crudo(self):
        rutas = [r["ruta"] for r in indice.buscar("floridablanca")]
        self.assertIn("areas/campuslands.md", rutas)
        self.assertNotIn("inbox/crudo.md", rutas)
        self.assertIn("inbox/crudo.md", [r["ruta"] for r in indice.buscar("floridablanca", incluir_crudo=True)])
        self.assertTrue(indice.buscar("alcaldia"))  # "alcaldía" en open-loops


class TestBotKapso(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import kapso_whatsapp_bot as bot
        cls.bot = bot
        cls.cliente = bot.app.test_client()

    def _post(self, cuerpo: dict, firmar: bool = True):
        raw = json.dumps(cuerpo).encode()
        headers = {"Content-Type": "application/json"}
        if firmar:
            headers["X-Webhook-Signature"] = hmac.new(SECRETO.encode(), raw, hashlib.sha256).hexdigest()
        return self.cliente.post("/webhook", data=raw, headers=headers)

    def _procesar_cola(self):
        while (fila := cola.tomar_siguiente()):
            self.bot.procesar_payload(json.loads(fila["payload"]))
            cola.marcar_hecho(fila["id"])

    def test_webhook_sin_firma_se_rechaza(self):
        r = self._post({"message": {"id": "x1", "from": ADMIN, "type": "text", "text": {"body": "hola"}}}, firmar=False)
        self.assertEqual(r.status_code, 401)

    def test_challenge_requiere_verify_token(self):
        self.assertNotEqual(self.cliente.get("/webhook?hub.challenge=abc").data, b"abc")
        self.assertEqual(self.cliente.get("/webhook?hub.challenge=abc&hub.verify_token=token-verificacion").data, b"abc")

    def test_tercero_queda_en_borrador_y_solo_sale_con_aprobacion(self):
        enviados = []
        with mock.patch.object(self.bot, "enviar_mensaje_kapso", side_effect=lambda to, t, phone_id=None: enviados.append(to) or True), \
             mock.patch.object(self.bot, "responder_como_diego", return_value="Hola, te cuento..."):
            r = self._post({"message": {"id": "t1", "from": TERCERO, "type": "text", "text": {"body": "¿cuánto cuesta?"}}})
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.get_json()["encolados"], 1)
            self._post({"message": {"id": "t1", "from": TERCERO, "type": "text", "text": {"body": "¿cuánto cuesta?"}}})
            self._procesar_cola()
            self.assertEqual(enviados, [ADMIN])  # al tercero no le llegó nada
            self.assertTrue((TMP / "inbox" / "whatsapp" / "otros" / f"{TERCERO}.md").exists())

            bid = cola.borradores_pendientes()[-1]["id"]
            self._post({"message": {"id": "a1", "from": ADMIN, "type": "text", "text": {"body": f"Editar {bid}: Hola, el costo lo confirma admisiones."}}})
            self._procesar_cola()
            self.assertEqual(enviados, [ADMIN, TERCERO, ADMIN])
            self.assertFalse([b for b in cola.borradores_pendientes() if b["id"] == bid])

    def test_admin_aprueba_propuestas_por_whatsapp(self):
        pid = cola.crear_propuesta("agregar_pendiente", {"texto": "Pendiente desde WhatsApp de prueba"}, "test")
        with mock.patch.object(self.bot, "enviar_mensaje_kapso", return_value=True):
            self._post({"message": {"id": "a2", "from": ADMIN, "type": "text", "text": {"body": f"Aceptar {pid}"}}})
            self._procesar_cola()
        self.assertIn("Pendiente desde WhatsApp de prueba", (TMP / "meta" / "open-loops.md").read_text(encoding="utf-8"))

    def test_remitente_vacio_no_es_admin(self):
        self.assertFalse(self.bot.es_administrador(""))
        self.assertFalse(self.bot.es_administrador("999"))
        self.assertTrue(self.bot.es_administrador("+57 300 000 0999"))


if __name__ == "__main__":
    unittest.main()
