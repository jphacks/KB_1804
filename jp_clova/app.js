const clova = require('@line/clova-cek-sdk-nodejs');
const express = require('express');

const clovaSkillHandler = clova.Client
    .configureSkill()

    //起動時に喋る
    .onLaunchRequest(responseHelper => {
        responseHelper.setSimpleSpeech({
            lang: 'ja',
            type: 'PlainText',
            value: 'はーい，わったいさま',
        });
    })

    //ユーザーからの発話が来たら反応する箇所
    .onIntentRequest(async responseHelper => {
        const intent = responseHelper.getIntentName();
        const sessionId = responseHelper.getSessionId();

        console.log('Intent:' + intent);
        if(intent === 'follow_me'){
          const slots = responseHelper.getSlots();
          //console.log(slots);
          //デフォルトのスピーチ内容を記載 - 該当スロットがない場合をデフォルト設定
          let speech = {
            lang: 'ja',
            type: 'PlainText',
            value: `わったいさん許してください．おねがいします．`
          }
/*          if(slots.area === '秋葉原'){
            speech.value = `${slots.area}のオススメのカレー屋は フジヤマドラゴンカレー です。`;
          }else if(slots.area === '神保町'){
            speech.value = `${slots.area}のオススメのカレー屋は 共栄堂 です。`;
          }else if(slots.area === '神田'){
            //神田のカレー情報検索
          //何か自分で書いてみましょう。
        }
*/
        responseHelper.setSimpleSpeech(speech);
        responseHelper.setSimpleSpeech(speech, true);
      }
    })

    //終了時
    .onSessionEndedRequest(responseHelper => {
        const sessionId = responseHelper.getSessionId();
    })
    .handle();


const app = new express();
const port = process.env.PORT || 3000;

//リクエストの検証を行う場合。環境変数APPLICATION_ID(値はClova Developer Center上で入力したExtension ID)が必須
const clovaMiddleware = clova.Middleware({applicationId: 'com.techtech.ubi'});
app.post('/clova', clovaMiddleware, clovaSkillHandler);

app.listen(port, () => console.log(`Server running on ${port}`));
