from flask import Flask
from flask_talisman import Talisman
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Configura cabeceras de seguridad HTTP para mitigar advertencias de OWASP ZAP:
# - X-Frame-Options (anti-clickjacking)
# - X-Content-Type-Options (anti MIME-sniffing)
# - Content-Security-Policy
# - Strict-Transport-Security
Talisman(
    app,
    force_https=False,        # deshabilitado porque corremos en HTTP local/Docker
    content_security_policy={
        "default-src": "'self'",
        "script-src": "'self'",
    },
    frame_options="DENY",
    x_content_type_options=True,
    referrer_policy="strict-origin-when-cross-origin",
    permissions_policy={
        "geolocation": "()",
        "microphone": "()",
        "camera": "()",
    },
)


@app.route("/")
def hola_mundo():
    return "Hola Mundo", 200


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)