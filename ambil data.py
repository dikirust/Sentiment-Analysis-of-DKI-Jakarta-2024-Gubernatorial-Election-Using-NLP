from googleapiclient.discovery import build
import pandas as pd

# Setup API Key dan YouTube API client
API_KEY = "YOUR_YOUTUBE_API_KEY"  # Ganti dengan API Key Anda
youtube = build("youtube", "v3", developerKey=API_KEY)

def search_videos(query, max_results=5):
    """Cari video berdasarkan nama."""
    response = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results
    ).execute()
    
    videos = []
    for item in response["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        videos.append({"video_id": video_id, "title": title})
    return videos

def get_video_comments(video_id, max_comments=50):
    """Ambil komentar dari video berdasarkan ID."""
    comments = []
    response = youtube.commentThreads().list(
        videoId=video_id,
        part="snippet",
        maxResults=100  # Maksimal 100 komentar per request
    ).execute()

    while response and len(comments) < max_comments:
        for item in response["items"]:
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            text = snippet["textDisplay"]
            author = snippet.get("authorDisplayName", "Unknown")  # Nama pembuat komentar
            comments.append({"comment": text, "author": author})

        # Ambil halaman berikutnya jika ada
        if "nextPageToken" in response:
            response = youtube.commentThreads().list(
                videoId=video_id,
                part="snippet",
                pageToken=response["nextPageToken"],
                maxResults=100
            ).execute()
        else:
            break
    return comments

# Main program
def main():
    # Ganti dengan nama video yang ingin dicari
    video_names = ["Debat Pilkada Jakarta 2024", "Debat Perdana Pilkada Jakarta 2024", "RK-Suswono, Dharma-Kun, Pramono-Rano", "Debat Gubernur Jakarta 2024"]
    all_comments = []

    for name in video_names:
        videos = search_videos(name, max_results=3)  # Cari hingga 3 video per nama
        for video in videos:
            print(f"Fetching comments for video: {video['title']} ({video['video_id']})")
            comments = get_video_comments(video["video_id"])
            for c in comments:
                all_comments.append({
                    "video_id": video["video_id"],
                    "title": video["title"],
                    "comment": c["comment"],
                    "author": c["author"]
                })
    
    # Simpan hasil ke CSV
    df = pd.DataFrame(all_comments)
    df.to_csv("Dataset Pilgub Jakarta.csv", index=False)
    print("Comments saved to Dataset Pilgub Jakarta.csv")

if __name__ == "__main__":
    main()
