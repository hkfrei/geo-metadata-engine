# Metadata Editor
![matadata](https://github.com/user-attachments/assets/da5b4aac-eb68-4a94-b6a9-563bd5c2177a)

This is the metadata editor for the WIS-BE project of the canton of Bern.
It's intention is to provide a plattform for for creating and retrieving metadata.
One of the main goals is to retrieve metadata as JSON, which can be used to create services and
WebMaps in ArcGIS Online.

## Prerequisites
To be able to run this project, you need a local **python** and **pip** installation.<br />
[Here](https://www.python.org/downloads/) you can find more information about it.

## Getting started

First, get a copy of the app to your local machine:
```
git clone https://github.com/hkfrei/bgi_metadata.git
cd bgi_metadata
```

## Install requirements

The project needs django and other libraries which need to be installed first.
```
pip install -r ./requirements.txt
```

## Start the development server
After the installation you can start the development server.<br />
In your console run the following command.
 ```
 python manage.py runserver
 ```
 open [http://localhost:8000/](http://localhost:8000/) to see the site running.

 ## Support
 To get support for this project please contact:
 
 **Kanton Bern**<br />
 Amt für Wald und Naturgefahren<br />
 Abteilung Fachdienste und Ressourcen<br />
 Bereich Geoinformation<br />

 ## Contributing
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
