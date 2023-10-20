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
          return ListView.builder(
            itemCount: data.length,
            itemBuilder: (BuildContext context, int i) => SearchResultWidget(
              SearchResultModel(
                title: data[i]["title"],
                channelName: data[i]["channel_name"],
                thumbnailUrl: data[i]["thumbnail_url"],
                videoId: data[i]["video_id"]
              )
            ),
          );
        }
    );
  }
}
