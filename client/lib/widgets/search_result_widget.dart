import 'package:flutter/material.dart';
import 'package:html_unescape/html_unescape.dart';
import 'package:ytd_web/api/api.dart';
import 'package:ytd_web/modals/search_result_model.dart';
import 'package:ytd_web/util/styles.dart';

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
              Row(
                children: [
                  FutureBuilder(
                      future: searchResultModel.channelThumbnailProvider,
                      builder: (context, snap) {
                        return CircleAvatar(
                          radius: 10.5,
                          backgroundColor: Styles.white,
                          backgroundImage: snap.data,
                          child: snap.data == null ? const Center(
                              child: Icon(
                                Icons.person,
                                size: 12.58,
                              )
                          ) : null,
                        );
                      }
                  ),
                  const SizedBox(width: 10,),
                  Expanded(
                    child: Text(
                        searchResultModel.channelName,
                        style: const TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.bold,
                            color: Styles.white,
                            fontFamily: Styles.fontFamily
                        ),
                        overflow: TextOverflow.ellipsis
                    ),
                  ),
                ],
              )
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
