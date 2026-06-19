#!/usr/bin/env python3
"""
Exporta slides do Soft Carrossel como PNGs 1080x1350.

Diferente do instagram-carousel: aqui o viewport real é 1080x1350,
não 420x525 escalado. Cada slide é um <div class="slide"> independente
de 1080x1350px. O script renderiza UM slide por vez no viewport e
captura screenshot.

Uso:
    python3 export_pngs.py \
      --html /caminho/preview.html \
      --output /caminho/output_dir
"""

import argparse
import asyncio
import sys
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Playwright não instalado. Rodando: pip install playwright && playwright install chromium")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright", "--break-system-packages"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    from playwright.async_api import async_playwright


SLIDE_WIDTH = 1080
SLIDE_HEIGHT = 1350


async def export_slides(html_path: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    html_content = html_path.read_text(encoding="utf-8")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": SLIDE_WIDTH, "height": SLIDE_HEIGHT},
            device_scale_factor=1,
        )

        await page.set_content(html_content, wait_until="networkidle")
        # Aguardar fontes do Google Fonts carregarem
        await page.wait_for_timeout(3000)

        # Remover o transform: scale do preview para exportar tamanho real
        await page.evaluate("""() => {
            // Remove o body padding e gap, mostra um slide por vez
            document.body.style.cssText = 'margin:0;padding:0;background:#fff;';

            // Reseta cada slide pra dimensão real, sem scale
            document.querySelectorAll('.slide').forEach(slide => {
                slide.style.transform = 'none';
                slide.style.marginBottom = '0';
                slide.style.boxShadow = 'none';
            });

            // Esconde os labels "SLIDE 1", "SLIDE 2" etc
            document.querySelectorAll('.slide-label').forEach(label => {
                label.style.display = 'none';
            });

            // Esconde todos os wrappers exceto o primeiro
            document.querySelectorAll('.slide-wrapper').forEach((w, i) => {
                w.style.gap = '0';
                if (i > 0) w.style.display = 'none';
            });
        }""")

        slides_count = await page.evaluate("document.querySelectorAll('.slide-wrapper').length")
        print(f"Encontrados {slides_count} slides para exportar.")

        for i in range(slides_count):
            # Mostra apenas o slide i
            await page.evaluate("""(idx) => {
                document.querySelectorAll('.slide-wrapper').forEach((w, j) => {
                    w.style.display = (j === idx) ? 'flex' : 'none';
                });
            }""", i)

            await page.wait_for_timeout(300)

            output_file = output_dir / f"slide_{i+1:02d}.png"
            await page.screenshot(
                path=str(output_file),
                clip={"x": 0, "y": 0, "width": SLIDE_WIDTH, "height": SLIDE_HEIGHT},
                omit_background=False,
            )
            print(f"  ✓ slide_{i+1:02d}.png")

        await browser.close()

    print(f"\nExportação concluída em: {output_dir}")
    return slides_count


def main():
    parser = argparse.ArgumentParser(description="Exporta slides do Soft Carrossel como PNGs 1080x1350")
    parser.add_argument("--html", required=True, type=Path, help="Caminho do preview.html")
    parser.add_argument("--output", required=True, type=Path, help="Diretório de saída dos PNGs")
    args = parser.parse_args()

    if not args.html.exists():
        print(f"Erro: arquivo HTML não encontrado: {args.html}", file=sys.stderr)
        sys.exit(1)

    asyncio.run(export_slides(args.html, args.output))


if __name__ == "__main__":
    main()
