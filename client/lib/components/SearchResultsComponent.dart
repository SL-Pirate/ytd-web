import 'package:flutter/material.dart';
import 'package:ytd_web/api/api.dart';
import 'package:ytd_web/modals/search_result_model.dart';
import 'package:ytd_web/widgets/search_result_widget.dart';

class SearchResultsComponent extends StatefulWidget {
  final String? searchTerm;
  const SearchResultsComponent(this.searchTerm, {super.key});

  @override
  State<SearchResultsComponent> createState() => _SearchResultsComponentState();
}

class _SearchResultsComponentState extends State<SearchResultsComponent> {
  @override
  Widget build(BuildContext context) {
    if (widget.searchTerm == null) {
      return const Center(
        child: Card(
          elevation: 4.0,
          margin: EdgeInsets.all(16.0),
          child: Padding(
            padding: EdgeInsets.all(16.0),
            child: Text(
              'Tap on the searchbar to start searching now',
              style: TextStyle(fontSize: 16.0),
              textAlign: TextAlign.center,
            ),
          ),
        ),
      );
    }
    return FutureBuilder(
        future: Api.instance.search(widget.searchTerm!),
        builder: (BuildContext context, AsyncSnapshot snapshot) {
          if (!snapshot.hasData) {
            return const Center(
                child: CircularProgressIndicator()
            );
          }
          List<dynamic> data = snapshot.data["results"];
          return SingleChildScrollView(
            child: Center(
              child: Column(
                children: [
                  for (var item in data)
                    SearchResultWidget(
                        SearchResultModel(
                            title: item["title"],
                            channelName: item["channel_name"],
                            thumbnailUrl: item["thumbnail_url"],
                            videoId: item["video_id"]
                        )
                    )
                ],
              ),
            ),
          );
        }
    );
  }
}
