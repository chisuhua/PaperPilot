"""
Create a test PDF for demonstration and testing purposes.
"""

import fitz  # PyMuPDF
from pathlib import Path


def create_test_pdf():
    """Create a sample academic paper PDF."""
    
    # Create a new PDF
    doc = fitz.open()
    page = doc.new_page()
    
    # Paper content
    content = """
Deep Learning for Image Recognition

Author: John Doe
Year: 2024

Abstract:
Deep learning has revolutionized image recognition in recent years. 
This paper explores the application of convolutional neural networks 
for image classification tasks. We demonstrate that deep learning 
models can achieve state-of-the-art performance on various benchmarks.

Introduction:
Neural networks have become the dominant approach in computer vision.
The key innovation is the use of multiple layers to learn hierarchical 
features from raw pixel data. This approach has shown remarkable success
in tasks such as object detection, image segmentation, and facial recognition.

Methods:
We trained a deep convolutional neural network with 50 layers on the 
ImageNet dataset. The model uses residual connections to facilitate 
training of very deep networks. Data augmentation techniques including
random cropping and horizontal flipping were applied during training.

Results:
Our model achieved 95% accuracy on the test set, outperforming previous
state-of-the-art methods. The learned features show strong generalization
to other image recognition tasks. Visualization of intermediate layers
reveals that the network learns increasingly complex features.

Conclusion:
Deep learning provides a powerful framework for image recognition.
Future work will explore transfer learning and few-shot learning scenarios.
The source code and trained models are available for research purposes.
"""
    
    # Insert text into the page
    rect = fitz.Rect(50, 50, 550, 750)
    page.insert_textbox(rect, content, fontsize=11, align=0)
    
    # Set metadata
    doc.set_metadata({
        'title': 'Deep Learning for Image Recognition',
        'author': 'John Doe',
        'subject': 'Deep Learning, Computer Vision',
        'keywords': 'deep learning, neural networks, image recognition',
        'creationDate': 'D:20240101000000'
    })
    
    # Ensure papers directory exists
    papers_dir = Path('papers')
    papers_dir.mkdir(exist_ok=True)
    
    # Save the PDF
    output_path = papers_dir / 'test_paper.pdf'
    doc.save(str(output_path))
    doc.close()
    
    print(f"✓ Test PDF created: {output_path}")
    print(f"  Title: Deep Learning for Image Recognition")
    print(f"  Author: John Doe")
    print(f"  Year: 2024")
    print(f"  Pages: 1")


if __name__ == "__main__":
    create_test_pdf()
