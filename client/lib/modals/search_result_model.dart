import 'package:flutter/widgets.dart';
import 'package:ytd_web/util/api.dart';

class SearchResultModel{
  final String videoId;
  final String title;
  final String? _thumbnailUrl;
  final String? description;
  final String channelName;
  final String? _channelThumbnailUrl;

  const SearchResultModel({
    required this.videoId,
    required this.title,
    this.description,
    required String? thumbnailUrl,
    required this.channelName,
    required String? channelThumbnailUrl,
  }) : _thumbnailUrl = thumbnailUrl,
        _channelThumbnailUrl = channelThumbnailUrl;

  Future<Image?> get thumbnail async {
    try{
      final bytes = await Api.instance.getImage(_thumbnailUrl!);
      return Image.memory(
        bytes,
        fit: BoxFit.fitWidth,
      );
    }
    catch(e){
      return null;
    }
  }

  Future<MemoryImage?> get thumbnailProvider async {
    try{
      final bytes = await Api.instance.getImage(_thumbnailUrl!);
      return MemoryImage(bytes);
    }
    catch(e){
      return null;
    }
  }

  Future<Image?> get channelThumbnail async {
    try{
      final bytes = await Api.instance.getImage(_channelThumbnailUrl!);
      return Image.memory(bytes);
    }
    catch(e){
      return null;
    }
  }

  Future<MemoryImage?> get channelThumbnailProvider async {
    try{
      final bytes = await Api.instance.getImage(_channelThumbnailUrl!);
      return MemoryImage(bytes);
    }
    catch(e){
      return null;
    }
  }
}