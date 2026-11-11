import asyncio
from playwright.async_api import async_playwright
import os

async def take_screenshots():
    html_file_path = r"d:\Empresa\opensquad\squads\rb-data-content-producer\output\2026-05-08-010237\v1\carrossel-visual-dark.html"
    output_dir = r"d:\Empresa\opensquad\squads\rb-data-content-producer\output\2026-05-08-010237\v1\slides"
    
    os.makedirs(output_dir, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Navigate to the local HTML file
        await page.goto(f"file:///{html_file_path}")
        
        # Wait for content to render, especially animations
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(2000) # Give extra time for any JS/animations

        slides = await page.query_selector_all('.slide')
        for i, slide in enumerate(slides):
            # Scroll the slide into view
            await slide.scroll_into_view_if_needed()
            # Give a small pause to ensure rendering is complete after scroll
            await page.wait_for_timeout(500)

            # Take screenshot of the individual slide element
            screenshot_path = os.path.join(output_dir, f"slide_{i+1:02d}.png")
            await slide.screenshot(path=screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(take_screenshots())
