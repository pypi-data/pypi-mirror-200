# Image Quality Assessment (IQA) Metrics Toolbox
 
## 1. Content

|metric|class|description|better|range|ref|
|:-|:-|:-|:-|:-|:-|
|Peak signal-to-noise ratio (PSNR)|FR|The ratio of the maximum pixel intensity to the power of the distortion.|higher|`[0, inf]`|[[WIKI]](https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio)|
|Structural similarity (SSIM) index|FR|Local similarity of luminance, contrast and structure of two image.|higher|`[0, 1]`|[[paper]](https://ieeexplore.ieee.org/document/1284395) [[WIKI]](https://en.wikipedia.org/wiki/Structural_similarity)|
|Blind/Referenceless Image Spatial QUality Evaluator|NR|Creates a mapping from features extracted from fitted generalised gaussian distributions to the final quality score using support vector machines to perform regression|higher|`[0, 100]`|[[paper]](https://ieeexplore.ieee.org/document/6272356)|
|Natural Image Quality Evaluator|NR|Distance between the quality aware NSS feature model and the
MVG fit to the features extracted from the distorted image|higher|`[0, 100]`|[[paper]](https://ieeexplore.ieee.org/document/6353522)|


## Installation

```bash
pip install IQA_Metrics_Toolbox
```
