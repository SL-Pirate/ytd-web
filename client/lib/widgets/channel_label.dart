import 'package:flutter/material.dart';
import 'package:ytd_web/modals/search_result_model.dart';
import 'package:ytd_web/util/styles.dart';

class ChannelLabel extends StatelessWidget {
  final SearchResultModel searchResultModel;
  const ChannelLabel({super.key, required this.searchResultModel});

  @override
  Widget build(BuildContext context) {
    return Row(
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
    );
  }
}

