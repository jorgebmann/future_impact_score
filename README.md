# Future impact score

Predict the number of future citations for research articles.

## Installation

Deploy this repository to a cloud computing or local unix platform.

```
git clone https://github.com/jorgebmann/future_impact_score
```

## Usage

Copy and paste an abstract of an research article and hit the calculate button.

## How It Works

This algorithm aims to predict the future number of citations based on the content of research articles. For this, Convolutional Neural Networks (CNN) were applied on a corpus of more than 500.000 papers, predicting the number of citations within the first two years after publication. Here, the trained CNN was provided to analyze its performance and to improve results.

## Background

The number of citations that a research article receives is a crucial measure for quality and importance of the underlying research output of that article. The number of citations has direct implications for the author’s track record, which has direct implications for grant and patent outputs. The prediction of future number of citations of a freshly published article would thus represent a crucial measure of the future impact of that article. Moreover, the prediction of future number of citations would also shed light on the author’s future impact on his/her field of research.


## Backtesting results

Results of this approach are quite promising: the model is able to predict the number of citations with an accuracy of up to 90%. A score with five categories was generated: from ‘very low future impact’ to ‘very high future impact’. Several different models were generated.
See https://aitextmaker.com/future-impact-score/ for further details.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)




