from flask import Flask, render_template, request, jsonify
import csv
import io

app = Flask(__name__)

# Define a function to filter and sum amounts by "Otsikko"
def filter_and_sum_by_otsikko(rows):
    result_dict = {}
    
    # Skip the header row
    header = rows[0]
    
    for row in rows[1:]:
        kirjauspaiva, maara, maksaja, maksunsaaja, nimi, otsikko, viitenumero, valuutta = row
        
        # Convert the "Maara" (amount) to a float and handle possible empty strings
        try:
            maara = float(maara.replace(',', '.'))
        except ValueError:
            maara = 0.0
        
        if otsikko in result_dict:
            result_dict[otsikko] += maara
        else:
            result_dict[otsikko] = maara
    
    # Convert the result dictionary to a list of tuples for easy formatting
    result_list = [(otsikko, sum) for otsikko, sum in result_dict.items()]
    
    return result_list

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('csv_files')
    result_messages = []

    csv_data = []
    
    for file in files:
        try:
            # Check if the file is a CSV
            if file.filename.endswith('.csv'):
                # Read CSV data
                csv_data = []
                with file.stream as csv_file:
                    # Read the file content as text with the appropriate encoding
                    file_content = csv_file.read().decode('utf-8')
                    
                    # Create a file-like object for the CSV reader
                    csv_file_object = io.StringIO(file_content)
                    
                    csv_reader = csv.reader(csv_file_object, delimiter=';', quotechar='"')
                    for row in csv_reader:
                        csv_data.append(row)

                # Extract and sum amounts by "Otsikko"
                filtered_and_summed_data = filter_and_sum_by_otsikko(csv_data)

                result_messages.append(f'File: {file.filename}')
                result_messages.append(f'Sum of Amounts by "Otsikko":\n{filtered_and_summed_data}')
            else:
                result_messages.append(f'Error: {file.filename} is not a CSV file')
        except Exception as e:
            result_messages.append(f'Error reading {file.filename}: {str(e)}')

    return jsonify({'message': '<br>'.join(result_messages)})

if __name__ == '__main__':
    app.run(debug=True)
