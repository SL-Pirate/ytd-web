import 'package:flutter/material.dart';
import 'package:ytd_web/modals/search_result_model.dart';
import 'package:ytd_web/screens/video_screen.dart';

class SearchResultWidget extends StatelessWidget {
  final SearchResultModel searchResultModel;

  const SearchResultWidget(this.searchResultModel, {super.key});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      child: Card(
        child: Column(
          children: [
            Text(searchResultModel.title),
            Image.network(searchResultModel.thumbnailUrl),
            Text(searchResultModel.channelName)
          ],
        ),
      ),
      onTap: () {
        Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => VideoScreen(searchResult: searchResultModel))
        );
      },
    );
  }
}
