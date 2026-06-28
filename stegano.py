from PIL import Image
import argparse

def text_to_binary(text):
    """Convert text to binary"""
    return ''.join(format(ord(char), '08b') for char in text) + '0000000000000000'

def analyze_image(image_path):
    with Image.open(image_path) as img:
        img=img.convert('RGB')
        width, height = img.size
        pixels = img.load()
        return pixels[0, 0], width, height

def modify_pixel(r, bit):
    r = (r & ~1) | int(bit)
    return r

def hide_text_in_image(image_path, text, output_path):
    binary_text = text_to_binary(text)

    with Image.open(image_path) as img:
        img = img.convert('RGB')
        width, height = img.size
        if len(binary_text) > width * height:
            raise ValueError("Text is too long to hide in this image.")
        pixels = img.load()

        binary_index = 0
        for y in range(height):
            for x in range(width):
                if binary_index < len(binary_text):
                    r, g, b = pixels[x, y]
                    r = modify_pixel(r, binary_text[binary_index])
                    pixels[x, y] = (r, g, b)
                    binary_index += 1
                else:
                    break
            if binary_index >= len(binary_text):
                break

        img.save(output_path)

def extract_text_from_image(image_path):
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        width, height = img.size
        pixels = img.load()

        binary_text = ''
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                binary_text += str(r & 1)

        # Split the binary string into chunks of 8 bits
        chars = [binary_text[i:i+8] for i in range(0, len(binary_text), 8)]
        text = ''
        for char in chars:
            if char == '00000000':
                break
            text += chr(int(char, 2))
        
        return text
    
def main():
    parser = argparse.ArgumentParser(
        description="Steganography: Hide and extract text in images.",
        epilog="Example usage:\n"
                "To hide text: python stegano.py hide input.png 'Secret Message' output.png\n"
                "To extract text: python stegano.py extract output.png",
                formatter_class=argparse.RawTextHelpFormatter
            )
    
    subparsers = parser.add_subparsers(dest='action', help='Available commands', required=True)

    hide_parser = subparsers.add_parser('hide', help='Hide text in an image')
    hide_parser.add_argument('image_path', type=str, help='Path to the input image')
    hide_parser.add_argument('text', type=str, help='Text to hide in the image')
    hide_parser.add_argument('output_path', type=str, help='Path to save the output image')

    extract_parser = subparsers.add_parser('extract', help='Extract text from an image')
    extract_parser.add_argument('image_path', type=str, help='Path to the input image')

    args = parser.parse_args()

    if args.action == 'hide':
        hide_text_in_image(args.image_path, args.text, args.output_path)
        print(f"Text hidden in {args.output_path}")
    elif args.action == 'extract':
        extracted_text = extract_text_from_image(args.image_path)
        print(f"Extracted text: {extracted_text}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()