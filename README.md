# Metadata Editor

![matadata](https://github.com/user-attachments/assets/da5b4aac-eb68-4a94-b6a9-563bd5c2177a)

This is the metadata editor for the WIS-BE project of the canton of Bern.
It's intention is to provide a plattform for for creating and retrieving metadata.
One of the main goals is to retrieve metadata as JSON, which can be used to create services and
WebMaps in ArcGIS Online.

## Prerequisites

To run this project, we recommend to use the **conda** package manager. <br />
[Here](https://docs.conda.io/en/latest/) you can find more information about it.

## Getting started

First, get a copy of the app to your local machine:

```
git clone https://github.com/hkfrei/bgi_metadata.git
cd bgi_metadata
```

## Create a virtual environment

It's recommended to run the application in a virtual python environment.
There are many ways to create one, but in this example we use conda.

```
conda create -n bgi_metadata python=3.12
```

after the environment was created, you can activate it.

```
conda activate bgi_metadata
```

## Install requirements

The project needs django and other libraries which need to be installed first. We recommend using conda cause arcgis is a conda package.

```
# First install esri::arcgis
conda install esri::arcgis
```

```
# Then install the packages from the requirements.txt file.
conda install --yes --file requirements.txt
```

## Apply the migrations

To apply the database migrations (schema), execute the following command.

```
python manage.py migrate
```

## Start the development server

After the installation you can start the development server.<br />
In your console run the following command.

```
python manage.py runserver
```

open [http://localhost:8000/](http://localhost:8000/) to see the site running.

## Docker

In case you want to run the app as a Docker container, there is a [Dockerfile](./Dockerfile) available.
If you have Docker installed on your machine, you can use the following commands to build and run the container.

```
# build the image
docker build -t bgi_metadata .

# run the container
docker run -d -p 8000:8000 bgi_metadata
```

Open [localhost:8000](http://localhost:8000) in your browser to see the app running.

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
