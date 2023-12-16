import 'package:flutter/material.dart';
import 'package:html_unescape/html_unescape.dart';
import 'package:ytd_web/util/api.dart';
import 'package:ytd_web/modals/search_result_model.dart';
import 'package:ytd_web/util/styles.dart';
import 'package:ytd_web/widgets/channel_label.dart';

class SearchResultWidget extends StatelessWidget {
  final SearchResultModel searchResultModel;
  const SearchResultWidget(this.searchResultModel, {super.key});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        SizedBox(
          width: 186,
          height: 109,
          child: FutureBuilder(
              future: searchResultModel.thumbnail,
              builder: (context, snapshot) {
                if (!snapshot.hasData) {
                  return Container(
                    color: Colors.black,
                    child: const Center(
                        child: CircularProgressIndicator()
                    ),
                  );
                }
                // return Placeholder();
                return snapshot.data!;
              }
          ),
        ),
        const SizedBox(width: 10,),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                  HtmlUnescape().convert(searchResultModel.title),
                  style: const TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: Styles.white,
                      fontFamily: Styles.fontFamily
                  )
              ),
              const SizedBox(height: 18,),
              ChannelLabel(searchResultModel: searchResultModel)
            ],
          ),
        )
      ],
    );
  }
}

dynamic child = Card(
  child: Column(
    children: [
      const Text("searchResultModel.title"),
      FutureBuilder(
          future: Api.instance.getImage("searchResultModel.thumbnailUrl"),
          builder: (context, snapshot) {
            if (!snapshot.hasData) {
              return const Center(
                  child: CircularProgressIndicator()
              );
            }
            // return Placeholder();
            return Image.memory(snapshot.data);
          }
      ),
      const Text("searchResultModel.channelName")
    ],
  ),
);
