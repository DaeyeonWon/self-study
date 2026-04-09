import os
import re
import glob

# Get all images
image_dir = '/Users/daniel.won/Workspace/self-study/assets/images_new/'
all_images = glob.glob(image_dir + '*.png')

# Extract page number for each image
page_image_map = {}
for img_path in all_images:
    basename = os.path.basename(img_path)
    match = re.search(r'page_(\d+)', basename)
    if match:
        page_num = int(match.group(1))
        if page_num not in page_image_map:
            page_image_map[page_num] = []
        page_image_map[page_num].append('assets/images_new/' + basename)

dir_path = '/Users/daniel.won/Workspace/self-study/'

# First grab what images are already present in the file to avoid duplicates in the same file
def extract_existing_images(content):
    return set(re.findall(r'src="?(assets/images_new/[^"]+)"?', content))

for i in range(1, 9):
    md_path = f'{dir_path}week{i}.md'
    if not os.path.exists(md_path): continue
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    existing_images = extract_existing_images(content)
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        new_lines.append(line)
        
        pages_to_add = set()
        
        # Catch PDF p.A-B
        for m in re.finditer(r'PDF p\.(\d+)-(\d+)', line):
            start, end = int(m.group(1)), int(m.group(2))
            for p in range(start, end+1): pages_to_add.add(p)
                
        # Catch PDF p.A (single)
        for m in re.finditer(r'PDF p\.(\d+)[^\-]', line + ' '):
            pages_to_add.add(int(m.group(1)))
            
        # Catch cite: A-B
        for m in re.finditer(r'cite:\s*(\d+)-(\d+)', line):
            start, end = int(m.group(1)), int(m.group(2))
            for p in range(start, end+1): pages_to_add.add(p)
                
        # Catch cite: A (single)
        for m in re.finditer(r'cite:\s*(\d+)(?!-)', line):
            pages_to_add.add(int(m.group(1)))
            
        # Catch cite: A, B (comma separated list manually parsing)
        for m in re.finditer(r'cite:\s*([\d,\s]+)\]', line):
            nums = m.group(1).split(',')
            for n in nums:
                try:
                    pages_to_add.add(int(n.strip()))
                except:
                    pass
            
        if pages_to_add:
            imgs_to_inject = []
            for p in sorted(pages_to_add):
                if p in page_image_map:
                    for img in sorted(page_image_map[p]):
                        if img not in existing_images:
                            imgs_to_inject.append(img)
                            existing_images.add(img) # Add to seen so we don't duplicate later
            
            if imgs_to_inject:
                img_tags = ''.join([f'<img src="{img}" width="30%" style="margin:5px; border-radius:8px; box-shadow:0 4px 6px rgba(0,0,0,0.1);">' for img in imgs_to_inject])
                new_lines.append(f'<div style="display:flex; flex-wrap:wrap; margin-top:10px; margin-bottom:20px;">\n{img_tags}\n</div>')
                
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
        
print("Successfully injected all referenced missing PDF images into the files!")
