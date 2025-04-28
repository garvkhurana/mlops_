from flask import Flask, render_template, request
import sys
import os
from network_security.constant.prediction_pipeline import CustomData, URLAnalyzer, PredictionPipeline
from network_security.exception.exception import NetworkSecurityException

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get("url")

        
        try:
            
            analyzer = URLAnalyzer()
            features_array = analyzer.extract_features(url)

            
            custom_data = CustomData(
                having_IP_Address=features_array[0][0],
                URL_Length=features_array[0][1],
                Shortining_Service=features_array[0][2],
                having_At_Symbol=features_array[0][3],
                double_slash_redirecting=features_array[0][4],
                Prefix_Suffix=features_array[0][5],
                having_Sub_Domain=features_array[0][6],
                SSLfinal_State=features_array[0][7],
                Domain_registeration_length=features_array[0][8],
                Favicon=features_array[0][9],
                port=features_array[0][10],
                HTTPS_token=features_array[0][11],
                Request_URL=features_array[0][12],
                URL_of_Anchor=features_array[0][13],
                Links_in_tags=features_array[0][14],
                SFH=features_array[0][15],
                Submitting_to_email=features_array[0][16],
                Abnormal_URL=features_array[0][17],
                Redirect=features_array[0][18],
                on_mouseover=features_array[0][19],
                RightClick=features_array[0][20],
                popUpWidnow=features_array[0][21],
                Iframe=features_array[0][22],
                age_of_domain=features_array[0][23],
                DNSRecord=features_array[0][24],
                web_traffic=features_array[0][25],
                Page_Rank=features_array[0][26],
                Google_Index=features_array[0][27],
                Links_pointing_to_page=features_array[0][28],
                Statistical_report=features_array[0][29]
            )

           
            input_df = custom_data.get_pandas_dataframe()

          
            pipeline = PredictionPipeline()
            prediction = pipeline.predict(input_df)

            result = "Malicious" if prediction[0] == -1 else "Safe"
            return render_template('index.html', result=result, url=url)
        
        except Exception as e:
            return render_template('index.html', result="Error", error_message=str(e))

    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)