import os
import yt_dlp
from pathlib import Path
from typing import Optional, Dict, List
from config.settings import YTDLP_OPTIONS, DOWNLOAD_DIR, MAX_FILE_SIZE


class VideoDownloader:
    """Handle video downloads using yt-dlp"""
    
    def __init__(self):
        self.download_dir = DOWNLOAD_DIR
    
    def extract_info(self, url: str) -> Optional[Dict]:
        """
        Extract video information without downloading
        
        Args:
            url: Video URL
        
        Returns:
            Video information dictionary or None if failed
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'nocheckcertificate': True,
            # Instagram specific options
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            print(f"Error extracting info: {e}")
            return None
    
    def get_formats(self, url: str) -> Optional[List[Dict]]:
        """
        Get available formats for a video
        
        Args:
            url: Video URL
        
        Returns:
            List of available formats or None if failed
        """
        info = self.extract_info(url)
        if not info:
            return None
        
        formats = info.get('formats', [])
        
        # Filter and sort formats
        filtered_formats = []
        for fmt in formats:
            # Skip formats without filesize info or that are too large
            filesize = fmt.get('filesize') or fmt.get('filesize_approx', 0)
            
            format_info = {
                'format_id': fmt.get('format_id'),
                'ext': fmt.get('ext'),
                'resolution': fmt.get('resolution', 'audio only'),
                'filesize': filesize,
                'vcodec': fmt.get('vcodec', 'none'),
                'acodec': fmt.get('acodec', 'none'),
                'format_note': fmt.get('format_note', ''),
                'width': fmt.get('width'),
                'height': fmt.get('height'),
            }
            filtered_formats.append(format_info)
        
        return filtered_formats
    
    def download(self, url: str, format_id: str = None, progress_callback=None) -> Optional[str]:
        """
        Download video with proper aspect ratio preservation
        
        Args:
            url: Video URL
            format_id: Specific format ID to download (optional)
            progress_callback: Callback function for download progress
        
        Returns:
            Path to downloaded file or None if failed
        """
        ydl_opts = YTDLP_OPTIONS.copy()
        
        if format_id:
            ydl_opts['format'] = format_id
        else:
            # Select best video+audio under 50MB, fallback to best under 50MB
            ydl_opts['format'] = '(bv*[filesize<50M]+ba[filesize<10M]/b[filesize<50M]/bv*[filesize<50M]+ba/b)[filesize<50M]/best'
        
        # Add progress hook if callback provided
        if progress_callback:
            ydl_opts['progress_hooks'] = [progress_callback]
        
        # Preserve aspect ratio - don't resize or crop
        ydl_opts['postprocessors'] = []
        
        # Add headers for Instagram and other sites
        ydl_opts['http_headers'] = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # Get the downloaded file path
                filename = ydl.prepare_filename(info)
                
                # Check file size
                if os.path.exists(filename):
                    file_size = os.path.getsize(filename)
                    if file_size > MAX_FILE_SIZE:
                        os.remove(filename)
                        return None
                    return filename
                
                return None
        except Exception as e:
            print(f"Error downloading: {e}")
            return None
    
    def download_best(self, url: str, progress_callback=None) -> Optional[str]:
        """
        Download best quality under file size limit
        Preserves original aspect ratio
        
        Args:
            url: Video URL
            progress_callback: Callback function for download progress
        
        Returns:
            Path to downloaded file or None if failed
        """
        return self.download(url, format_id=None, progress_callback=progress_callback)
    
    def download_medium(self, url: str, progress_callback=None) -> Optional[str]:
        """
        Download medium quality (480p-720p) under file size limit
        
        Args:
            url: Video URL
            progress_callback: Callback function for download progress
        
        Returns:
            Path to downloaded file or None if failed
        """
        ydl_opts = YTDLP_OPTIONS.copy()
        ydl_opts['format'] = '(bv*[height<=720][height>=480]+ba/b[height<=720][height>=480])[filesize<50M]/best[filesize<50M]'
        
        ydl_opts['http_headers'] = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        
        if progress_callback:
            ydl_opts['progress_hooks'] = [progress_callback]
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                if os.path.exists(filename):
                    file_size = os.path.getsize(filename)
                    if file_size > MAX_FILE_SIZE:
                        os.remove(filename)
                        return None
                    return filename
                
                return None
        except Exception as e:
            print(f"Error downloading medium quality: {e}")
            return None
    
    def download_low(self, url: str, progress_callback=None) -> Optional[str]:
        """
        Download low quality (360p or below) under file size limit
        
        Args:
            url: Video URL
            progress_callback: Callback function for download progress
        
        Returns:
            Path to downloaded file or None if failed
        """
        ydl_opts = YTDLP_OPTIONS.copy()
        ydl_opts['format'] = '(bv*[height<=360]+ba/b[height<=360])[filesize<50M]/worst[filesize<50M]'
        
        ydl_opts['http_headers'] = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        
        if progress_callback:
            ydl_opts['progress_hooks'] = [progress_callback]
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                if os.path.exists(filename):
                    file_size = os.path.getsize(filename)
                    if file_size > MAX_FILE_SIZE:
                        os.remove(filename)
                        return None
                    return filename
                
                return None
        except Exception as e:
            print(f"Error downloading low quality: {e}")
            return None
    
    def download_audio(self, url: str, progress_callback=None) -> Optional[str]:
        """
        Download audio only and convert to MP3
        
        Args:
            url: Video URL
            progress_callback: Callback function for download progress
        
        Returns:
            Path to downloaded file or None if failed
        """
        ydl_opts = YTDLP_OPTIONS.copy()
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        
        # Use writethumbnail and embed for better audio metadata
        ydl_opts['writethumbnail'] = False
        
        ydl_opts['http_headers'] = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        
        if progress_callback:
            ydl_opts['progress_hooks'] = [progress_callback]
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # Get the downloaded file path (with .mp3 extension)
                filename = ydl.prepare_filename(info)
                audio_filename = Path(filename).with_suffix('.mp3')
                
                if audio_filename.exists():
                    file_size = os.path.getsize(audio_filename)
                    if file_size > MAX_FILE_SIZE:
                        os.remove(audio_filename)
                        return None
                    return str(audio_filename)
                
                return None
        except Exception as e:
            print(f"Error downloading audio: {e}")
            return None
    
    def cleanup_file(self, filepath: str):
        """Delete downloaded file and any related files"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
            
            # Also cleanup any thumbnail or metadata files
            base_path = Path(filepath)
            for ext in ['.jpg', '.png', '.webp', '.json', '.part']:
                related_file = base_path.with_suffix(ext)
                if related_file.exists():
                    os.remove(related_file)
        except Exception as e:
            print(f"Error cleaning up file: {e}")