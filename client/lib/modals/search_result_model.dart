class SearchResultModel{
  final String title;
  final String channelName;
  final String thumbnailUrl;
  final String videoId;

  const SearchResultModel({
    required this.title,
    required this.videoId,
    required this.channelName,
    required this.thumbnailUrl
  });
}