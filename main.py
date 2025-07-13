import os
import easyocr
from natsort import natsorted


def executar_ocr(imagem_path, reader):
    results = reader.readtext(imagem_path)
    texto = ""
    for _, text, _ in results:
        texto += f"{text}\n"
    return texto


def processar_pasta(pasta_imagens: str, pasta_saida: str, linguagem, concatenar_resultados: bool, gpu_use: bool):
    os.makedirs(pasta_saida, exist_ok=True)
    reader = easyocr.Reader(linguagem, gpu=gpu_use)
    imagens = [f for f in os.listdir(pasta_imagens) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    imagens = natsorted(imagens)
    total = len(imagens)

    if concatenar_resultados:
        saida_txt = os.path.join(pasta_saida, 'resultado_completo.txt')
        with open(saida_txt, 'a', encoding='utf-8') as f:
            for i, img_nome in enumerate(imagens, start=1):
                caminho_img = os.path.join(pasta_imagens, img_nome)

                texto = executar_ocr(caminho_img, reader)

                f.write(texto)

                print(f"\rProgresso: {((i / total) * 100):.1f}%", end='')

    else:
        for i, img_nome in enumerate(imagens, start=1):
            caminho_img = os.path.join(pasta_imagens, img_nome)
            nome_base = os.path.splitext(img_nome)[0]
            saida_txt = os.path.join(pasta_saida, f"{nome_base}.txt")

            texto = executar_ocr(caminho_img, reader)

            with open(saida_txt, 'w', encoding='utf-8') as f:
                f.write(texto)

            print(f"\rProgresso: {((i / total) * 100):.1f}%", end='')

    temp_img = "temp/temp_ocr_img.png"
    if os.path.exists(temp_img):
        os.remove(temp_img)


if __name__ == "__main__":
    try:
        pasta_imagens = "imagens"
        pasta_saida = "resultados_ocr"
        linguagem = ['en','pt']
        concatenar_resultados = True
        gpu_use = False
        print("Iniciando processamento de OCR em lote...")
        processar_pasta(pasta_imagens, pasta_saida, linguagem, concatenar_resultados, gpu_use)
        print("OCR finalizado para todas as imagens!")
    except Exception as e:
        print(f"\n Ocorreu um erro durante a execução: {e}")
