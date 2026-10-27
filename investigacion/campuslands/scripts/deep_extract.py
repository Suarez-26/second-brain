import os
import re
import json
import subprocess
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

OUT_DIR = r"c:\Users\tomas\second-brain\sources\prensa_y_web"

# 1. Read all art_*.txt files that succeeded and extract their main article body
art_files = [f for f in os.listdir(OUT_DIR) if f.startswith("art_") and f.endswith(".txt")]
articles_clean = {}
for af in sorted(art_files):
    p = os.path.join(OUT_DIR, af)
    with open(p, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    # Skip binary PDF dumps
    if "%PDF-" in content[:1000]:
        continue
    articles_clean[af] = content

with open(os.path.join(OUT_DIR, "all_downloaded_articles.json"), "w", encoding="utf-8") as f:
    json.dump(articles_clean, f, ensure_ascii=False, indent=2)

print(f"Compiled {len(articles_clean)} non-PDF text articles.")

# 2. Resolve new vertexaisearch URLs from latest batch
NEW_URLS = [
    ("ramajudicial_gbp", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFDCJL6o3lm0LWenbfPx7iyH3AO7fXgBwURQ-pAg6CTU8WxFK4lBUcey2aVj_7zpKhMzOhSnrN679SvEKmsJ1GcOpGnDazcG0bwrp8_3WpkzzwJXkmTmMyuL0bmwus2VKHPCB-ggIcS1cbRsK1KSRj71HAq-RnZU9ksNoWcy6CWJvl6TNnNgJDjgOH_sGB1zrPxzt2k3TQocYiGLm0OmGPXswioRP3w"),
    ("informacolombia_gbp", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGUWkjcFUKhzLX5QoUYBIghcaADXb6PL6G-G5giuibuQ_bN_h3rCgGC8WepRxs1yWK3w1jSDBgMzXq8be3cZyLQjoR6i3kBhyajGOB0591w1hRdRwHnqae3-4vZItYDlyGSx26Scizc_iSt8XxJ_e0hzK64yIWwh9GrQe62k1aYK2TsUpFmsm-EiZthLK1qL3tGg_3lBODTpAFbTAfDWcE1t5CmssjaGVv2O-Mgtl86atMTqmGjYBgth2PEwWtYiSYXT8G6FZ4lK-VmSlqWIMXVMbuT168XQqmbUs9dtTPz1Z4c7br8-E5bQ1-boGVrPuaMhc_5FhKRKKxIDPOiIzcffyIW7L-pjZrr"),
    ("vanguardia_leeche_2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEjSzw78knXHaxnedRmGBJOyjLVPNLqcToINrnE3X8Iti2-xqn-Q8rtLWAaFVkZ3JfKUU6-w5ZXMQc91EEtLaHMHRyiq6yeRSOfzKi2GlnM0Qtw0fQ87tO2i77HU5Y5EopQtTo3I3oJ8rJMte8OtekryBbV6gIa_vpt5nNSM4-I-3LFWSwQFFCRxdm5-xDKkK9rnFTZ8sB6r6dAjRbzVwHU"),
    ("zonafranca_hubux", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHrRESVYDyyFyZ8UtR3OIvZKryhkKDkkZc2d1axoIVZIKTWbinhIoeVWAIgQFE2rkG5Wg98llrtqsHdp95A1GXQDjdg6sUk7X4VGdaqEF8jMmG0KFxX6Qjb4WWBEwlYBg-IBLvaDU2_ujNeYoAY"),
    ("magneto_hubux_2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGYJzzFGGXYhYQ2jkzAbRWxSgzLvXU30PxbXnf7WCZ3hLLpblJAb6K_FLYLs59UMy7MuK33T0AvOMzd_ragPOLFsl9D-qauR-7Qir-xkzrtrqOij3T98twFL23otaOqXqxdfxVhnrKU0zNacqJi37bq890udH3b8M2PnULUuLkP222Xq6a1krwS"),
    ("metropolitano_new_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHqUiC17Rff717injt19JUjZDNQw6k9cjWWvdSueDejUFcOTRtkaYjK5e6JctzShLAv_51QcpS35F2NMwjK7ujbK7xzyAui83kBkB6V8v-pbltj7cI_R5pvYIlkBwPIjtdIbvUS6y-sb_VhXZw09LTtwZcoNclxatKlzEpQSZevmpzYBrUxEmMHyBnT2GfcmuHRHS9zFLzzaAzeEZGh2qd5EntYjwJd6HKWaA=="),
    ("metropolitano_new_2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGy8ZczhDreXmPDCHcYXvja4OgddAsNP4eS-SWf4FwuTkFDUsj5mHWQCoNNhnLEboPgWtol5kp8uOjL8AQ9J73qgyH-oKDekvGeZUOHc-OzoZ1ZsDD1cCS_AFoWeVtq8WtQQ9-_G3he0BQBwtZ_W-aWcr4eBwqHESLjVOL5-7DPle1EJrJ2Q0nUHnomqDDKA3AQ"),
    ("metropolitano_2026_10_09", "https://metropolitano.com.co/adoptar-inteligencia-artificial-es-cuestion-de-supervivencia-para-las-empresas-diego-tarazona-ceo-de-campuslands/"),
    ("metropolitano_2026_04_24", "https://metropolitano.com.co/campuslands-generara-400-empleos-en-tecnologia-en-bucaramanga/"),
    ("metropolitano_2025_10_07", "https://metropolitano.com.co/gobernacion-firma-convenio-con-campuslands-para-formacion-de-200-jovenes-programadores/"),
    ("fedesoft_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH75sIdStLtR52gRCQMrBHHAEhZAKel4ZhuyHH6KShF_ft5LH3PBz43Yf9uq0S-E-72NMedEmLonMsr5yhdGIKVjnHZhRLool1dt1N97IufFvADFSYGTSExry4="),
    ("fedesoft_2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHt3Tc9pqV11U8PsUBLmIT15IbLmu2iNvVCI0shNeqdAUjjojV2PyyIwbuHf7dW0a7hjfOgevh3s3WdAhZYe3bs-evY0jXNEsaHie_rrjMHSd1I"),
    ("fedesoft_3", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH9LaZEQovaVnbbcwmnuAzpCzk_L7p7AGnhOYMlpAd0sGOw7-YfUic0z6UX2KhTCseJeJCt2aOmGPqJR0491a_6i_viSW_3MOxStER2dYW77fEHncoyhmproAkyDoxT-5dWtesq6hu2tZU="),
    ("fedesoft_4", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE13iKESN2zjtlbcPhleHwA2FGe6FZl_fEP_dZ1mWk4jKS_3eITYEH9ETrP3C5_-D4eegxG9Lf5F_ZS6HszAAgcT-COD9i6-Xc8s3vqOUX9tvP7vY6vKrEUHkXUFbFFuI73U-uu7xqgs13frxQO3PhlokRT-NY4FhUGVgB33cRJaFvmpnA5e7ia3jt30gwtc6bJf5e2JFkjp6n7dXF7STBl2YZ8YYSThqXjHQ=="),
    ("fedesoft_5", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFZ_YfJB41lV2pdMWemfChDrIDuAceB7Bt_ThtX4v7SNNVCjj2VsJJgxe860QJnlD8i0bDnJr8f-rS1CzKdjM4tH2xENovh8C2juctZrahmObV9DFGa7tNb4a269IfePdSrcOiu4fVjfBilvtGKrBCl5Lzlca_B2tw1xzwbftO-bGvl_2djbmydRtI0Hs3mXC3N4EyBC_5qzVsJHQm5"),
    ("fedesoft_dir_1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH_F6q22vGjAkG6ZrWHN-55FBQ6QDLtmZoGaA-GPRaXyE2_A6qFBy5rrSLa04hqZeGO3gGwi4Ox62CDWp03pqrdkFMbzWnY2aTlxf4NaamnQ3OOHGc7nMx4f17z4RMEKsQz3bo08t6zkec=")
]

def clean_html(html):
    t = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    t = re.sub(r"<style[^>]*>.*?</style>", " ", t, flags=re.DOTALL | re.IGNORECASE)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

curl_results = []
for key, u in NEW_URLS:
    try:
        cmd = [
            "curl.exe", "-s", "-L", "--max-time", "15",
            "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "-w", "\n__FINAL_URL__:%{url_effective}",
            u
        ]
        proc = subprocess.run(cmd, capture_output=True)
        out = proc.stdout.decode("utf-8", errors="replace")
        final_u = u
        if "__FINAL_URL__:" in out:
            body, final_u = out.rsplit("__FINAL_URL__:", 1)
            final_u = final_u.strip()
        else:
            body = out
        clean = clean_html(body) if not body.startswith("%PDF") else "[PDF BINARY]"
        with open(os.path.join(OUT_DIR, f"curl_{key}.txt"), "w", encoding="utf-8") as f:
            f.write(f"KEY: {key}\nFINAL_URL: {final_u}\n\n{clean}")
        curl_results.append({"key": key, "final_url": final_u, "len": len(clean), "snippet": clean[:1200]})
    except Exception as e:
        curl_results.append({"key": key, "error": str(e)})

# 3. Try Arctic Shift & PullPush for Reddit threads 1v037ud, 1bj3jrq, 1om29x8
reddit_ids = ["1v037ud", "1bj3jrq", "1om29x8"]
arctic_out = {}
for rid in reddit_ids:
    for api_u in [
        f"https://arctic-shift.photon-reddit.com/api/posts/ids?ids={rid}",
        f"https://arctic-shift.photon-reddit.com/api/comments/tree?link_id=t3_{rid}&limit=100",
        f"https://api.pullpush.io/reddit/search/submission/?ids={rid}",
        f"https://api.pullpush.io/reddit/search/comment/?link_id={rid}&size=100"
    ]:
        try:
            cmd = ["curl.exe", "-s", "-L", "--max-time", "10", "-A", "Mozilla/5.0", api_u]
            proc = subprocess.run(cmd, capture_output=True)
            txt = proc.stdout.decode("utf-8", errors="replace")
            if txt and len(txt) > 20 and txt.strip().startswith("{"):
                arctic_out[f"{rid}_{api_u.split('/')[2]}_{api_u.split('/')[4].split('?')[0]}"] = json.loads(txt)
        except Exception as e:
            pass

with open(os.path.join(OUT_DIR, "curl_and_arctic_results.json"), "w", encoding="utf-8") as f:
    json.dump({"curl": curl_results, "reddit_archive": arctic_out}, f, ensure_ascii=False, indent=2)

print("Saved curl_and_arctic_results.json, curl items:", len(curl_results), "arctic keys:", list(arctic_out.keys()))
