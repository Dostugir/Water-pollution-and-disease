# Water Quality Prediction System

A web-based application that predicts water quality and safety using machine learning. The system analyzes various water parameters to determine if the water is safe for consumption.

## Features

- Real-time water quality prediction
- Analysis of multiple water parameters:
  - pH Level
  - Turbidity (NTU)
  - Nitrate concentration (mg/L)
  - Lead concentration (µg/L)
  - Dissolved Oxygen (mg/L)
- User-friendly web interface
- Detailed recommendations based on water parameters
- Confidence score for predictions

## Technical Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Machine Learning**: Random Forest Classifier
- **Data Processing**: NumPy, Pandas

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd Water-pollution-and-disease
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Enter the water parameters in the form:
   - pH Level (0-14)
   - Turbidity in NTU
   - Nitrate concentration in mg/L
   - Lead concentration in µg/L
   - Dissolved Oxygen in mg/L

4. Click "Predict Water Quality" to get the analysis

## Water Quality Standards

The system uses the following standards for water quality assessment:
- pH: Optimal range 6.5-8.5
- Turbidity: WHO standard < 1 NTU
- Nitrate: WHO standard < 10 mg/L
- Lead: WHO standard < 10 µg/L
- Dissolved Oxygen: WHO standard > 5 mg/L

## Project Structure

```
Water-pollution-and-disease/
├── app.py                 # Main Flask application
├── rf_model.pkl          # Trained Random Forest model
├── templates/
│   └── index.html        # Web interface
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```
![Screenshot 2025-05-03 235012](https://github.com/user-attachments/assets/97e37035-c190-41fc-b562-f35a99cbd884)

![Screenshot 2025-05-03 235048](https://github.com/user-attachments/assets/e1c1e33f-d216-49ba-b62a-618011f09713)

![Screenshot 2025-05-03 235220](https://github.com/user-attachments/assets/6987d450-dbad-40f8-bccb-fa4156b9be4d)


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- World Health Organization (WHO) water quality standards
- Machine learning model training data sources
- Flask web framework
