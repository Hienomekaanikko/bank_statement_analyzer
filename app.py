from flask import Flask, render_template, request, jsonify
import csv
import io

app = Flask(__name__)

def filter_and_sum_by_otsikko(rows):
    result_dict = {}
    header = rows[0]

    for row in rows[1:]:
        kirjauspaiva, maara, maksaja, maksunsaaja, nimi, otsikko, viitenumero, valuutta = row
        try:
            maara = float(maara.replace(',', '.'))
        except ValueError:
            maara = 0.0

        if otsikko in result_dict:
            result_dict[otsikko]['maara'] += maara
        else:
            result_dict[otsikko] = {
                'kirjauspäivä': kirjauspaiva,
                'otsikko': otsikko,
                'maara': maara
            }

    result_list = [(event['kirjauspäivä'], event['otsikko'], event['maara']) for event in result_dict.values()]

    result_list.sort(key=lambda x: x[2])  

    return result_list

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('csv_files')
    result_messages = []

    for file in files:
        try:
            if file.filename.endswith('.csv'):
                csv_data = []
                with file.stream as csv_file:
                
                    file_content = csv_file.read().decode('utf-8')
             
                    csv_file_object = io.StringIO(file_content)
                    
                    csv_reader = csv.reader(csv_file_object, delimiter=';', quotechar='"')
                    for row in csv_reader:
                        csv_data.append(row)

                filtered_and_summed_data = filter_and_sum_by_otsikko(csv_data)

                result_message = f'File: {file.filename}\n'
                result_message += 'Sum of Amounts by "Otsikko":\n'
                for event in filtered_and_summed_data:
                    result_message += f'Kirjauspäivä: {event[0]}\n'
                    result_message += f'Otsikko: {event[1]}\n'
                    result_message += f'Määrä: {event[2]} EUR\n\n'

                result_messages.append(result_message)
            else:
                result_messages.append(f'Error: {file.filename} is not a CSV file')
        except Exception as e:
            result_messages.append(f'Error reading {file.filename}: {str(e)}')

    return jsonify({'message': '<br>'.join(result_messages)})

if __name__ == '__main__':
    app.run(debug=True)
