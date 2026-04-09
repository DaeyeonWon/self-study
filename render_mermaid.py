import os
import re

dir_path = '/Users/daniel.won/Workspace/self-study/'
images_dir = os.path.join(dir_path, 'assets', 'images_new')
os.makedirs(images_dir, exist_ok=True)

# Pattern to find mermaid blocks:
# We find everything between ```mermaid and ```
mermaid_pattern = re.compile(r'```mermaid\n(.*?)\n```', re.DOTALL)

for i in range(1, 9):
    md_path = f'{dir_path}week{i}.md'
    if not os.path.exists(md_path): continue
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = mermaid_pattern.findall(content)
    if not blocks:
        continue
        
    for j, block in enumerate(blocks):
        # Create temp mmd file
        temp_mmd = f'/tmp/temp_mermaid_w{i}_{j}.mmd'
        out_png = f'assets/images_new/mermaid_w{i}_{j}.png'
        abs_out_png = os.path.join(dir_path, out_png)
        
        with open(temp_mmd, 'w', encoding='utf-8') as f:
            f.write(block)
            
        # Run mmdc command
        print(f"Compiling mermaid for week {i} block {j}...")
        res = os.system(f"cd {dir_path} && npx -y @mermaid-js/mermaid-cli -i {temp_mmd} -o {abs_out_png} -b transparent")
        
        if res == 0 and os.path.exists(abs_out_png):
            # Replace exactly that block in the text with image
            original_match = f"```mermaid\n{block}\n```"
            # Responsive HTML styling for the generated image
            img_tag = f'<br>\n<img src="{out_png}" width="80%" style="margin: 10px 0; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); background-color: white; padding: 10px;">\n<br>'
            content = content.replace(original_match, img_tag)
        else:
            print(f"Failed to compile mermaid image: week {i} block {j}")

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Mermaid block extraction, compilation, and replacement completed.")
