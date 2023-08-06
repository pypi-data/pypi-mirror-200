from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2 import service_account
from colors_terminal import Colors

class YTAPI:
    def __init__(self, credentials_file):
        self.creds = service_account.Credentials.from_service_account_file(credentials_file)

        # Construir el cliente de la API de YouTube
        self.youtube = build('youtube', 'v3', credentials=self.creds)

    def search_channels(self, query, max_results=20):
        try:
            # Realizar una búsqueda de canales por palabras clave
            request = self.youtube.search().list(
                q=query,
                type='channel',
                part='id',
                maxResults=max_results
            )
            response = request.execute()

            # Extraer los IDs de los canales de la lista de resultados
            channel_ids = [result['id']['channelId'] for result in response['items']]

            # Devolver los IDs de los canales encontrados
            return channel_ids
        except HttpError as error:
            if error.resp.status == 403:
                Colors.print("ERROR 403: The YouTube Data API v3 is not enabled for this project.", color="RED", style="BOLD")
            else:
                Colors.print(f"An error occurred while searching for videos: {error}", color="RED", style="BOLD")
            return None
        
    def get_channel_details(self, channel_id):
        try:
            request = self.youtube.channels().list(
                part='snippet,statistics',
                id=channel_id
            )
            response = request.execute()
            return response['items'][0]
        except HttpError as error:
            if error.resp.status == 403:
                Colors.print("ERROR 403: The YouTube Data API v3 is not enabled for this project.", color="RED", style="BOLD")
            else:
               Colors.print(f"An error occurred while searching for videos: {error}", color="RED", style="BOLD")
            return None


    def search_videos(self, query, max_results=20):
        try:
            # Realizar una búsqueda de videos por palabras clave
            request = self.youtube.search().list(
                q=query,
                type='video',
                part='id,snippet',
                maxResults=max_results
            )
            response = request.execute()

            # Devolver los resultados de la búsqueda
            return response['items']
        except HttpError as error:
            if error.resp.status == 403:
                Colors.print("ERROR 403: The YouTube Data API v3 is not enabled for this project.", color="RED", style="BOLD")
            else:
                Colors.print(f"An error occurred while searching for videos: {error}", color="RED", style="BOLD")
            return None
        
    def search_new_videos(self, channel_id, query=None, max_results=20):
        try:
            # Realizar una búsqueda de videos en un canal por palabras clave, ordenados por fecha de publicación
            request = self.youtube.search().list(
                q=query,
                type='video',
                channelId=channel_id,
                part='id,snippet',
                maxResults=max_results,
                order='date'
            )
            response = request.execute()

            # Obtener los videos de la lista de resultados, ordenados por fecha de publicación de manera ascendente (el más reciente primero)
            videos = sorted(response['items'], key=lambda x: x['snippet']['publishedAt'])

            # Devolver los videos ordenados por fecha de publicación de manera descendente (el más reciente primero)
            return videos[::-1]
        except HttpError as error:
            if error.resp.status == 403:
                Colors.print("ERROR 403: The YouTube Data API v3 is not enabled for this project.", color="RED", style="BOLD")
            else:
                Colors.print(f"An error occurred while searching for videos: {error}", color="RED", style="BOLD")
            return None

    def get_video_details(self, video_id):
        try:
            # Obtener los detalles de un video específico
            request = self.youtube.videos().list(
                id=video_id,
                part='id,snippet,statistics'
            )
            response = request.execute()

            # Devolver los detalles del video
            return response['items'][0]
        except HttpError as error:
            if error.resp.status == 403:
                Colors.print("ERROR 403: The YouTube Data API v3 is not enabled for this project.", color="RED", style="BOLD")
            else:
                Colors.print(f"An error occurred while searching for videos: {error}", color="RED", style="BOLD")
            return None