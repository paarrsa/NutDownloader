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
            }
            filtered_formats.append(format_info)
        
        return filtered_formats
    
    def download(self, url: str, format_id: str = None, progress_callback=None) -> Optional[str]:
        """
        Download video
        
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
        
        # Add progress hook if callback provided
        if progress_callback:
            ydl_opts['progress_hooks'] = [progress_callback]
        
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
        
        Args:
            url: Video URL
            progress_callback: Callback function for download progress
        
        Returns:
            Path to downloaded file or None if failed
        """
        return self.download(url, format_id=None, progress_callback=progress_callback)
    
    def download_audio(self, url: str, progress_callback=None) -> Optional[str]:
        """
        Download audio only
        
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
        
        if progress_callback:
            ydl_opts['progress_hooks'] = [progress_callback]
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # Get the downloaded file path (with .mp3 extension)
                filename = ydl.prepare_filename(info)
                audio_filename = Path(filename).with_suffix('.mp3')
                
                if audio_filename.exists():
                    return str(audio_filename)
                
                return None
        except Exception as e:
            print(f"Error downloading audio: {e}")
            return None
    
    def cleanup_file(self, filepath: str):
        """Delete downloaded file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"Error cleaning up file: {e}")