const clova = require('@line/clova-cek-sdk-nodejs');
const express = require('express');

const app = new express();
const port = process.env.PORT || 3000;

var n = 0;

app.get('/rpi' + String(n), function (req, res, next) {
  res.send('yyy_' + String(n));
  //next();
});

// request.post({
//   url:     'https://4b9a3cba.ngrok.io',
//   form:    { mes: "heydude" }
// }, function(error, response, body){
//   console.log(body);
// });

const clovaSkillHandler = clova.Client
    .configureSkill()

    //起動時に喋る
    .onLaunchRequest(responseHelper => {
      responseHelper.setSimpleSpeech({
          lang: 'ja',
          type: 'PlainText',
          value: 'てくてくクローバを起動しました',
      });
      app.get('/rpi' + String(n), function (req, res, next) {
        res.send('none_' + String(n));
        //next();
      });
      n++;
    })


    //ユーザーからの発話が来たら反応する箇所
    .onIntentRequest(async responseHelper => {
      const intent = responseHelper.getIntentName();
      const sessionId = responseHelper.getSessionId();
      console.log('Intent:' + intent);

      //デフォルト
      let speech = {
        lang: 'ja',
        type: 'PlainText',
        value: ``
      }
      const slots = responseHelper.getSlots();

      switch (intent) {
        case 'follow_me':
          //console.log(slots);
          speech.value = `待ってー，今行くね`;
          //ラズパイが/rpiにGETを送るとrunを返す
          app.get('/rpi'+ String(n), function (req, res, next) {
            res.send('run_' + String(n));
            //next();
          });
          console.log('run' + String(n));
          break;

        case 'stop_clova':
          //const slots = responseHelper.getSlots();
          //console.log(slots);
          speech.value = `分かった、止まるね`;
          //ラズパイが/rpiにGETを送るとstopを返す
          app.get('/rpi'+ String(n), function (req, res, next) {
            res.send('stop_'+ String(n));
            //next();
          });
          console.log('stop'+ String(n));
          break;

        default:
          speech.value = `ごめん、もう一回言って？`;

      }
      responseHelper.setSimpleSpeech(speech);
      responseHelper.setSimpleSpeech(speech, true);
      n = n + 1;
    })

    //終了時
    .onSessionEndedRequest(responseHelper => {
        const sessionId = responseHelper.getSessionId();
    })
    .handle();

// const app = new express();
// const port = process.env.PORT || 3000;

//リクエストの検証を行う場合。環境変数APPLICATION_ID(値はClova Developer Center上で入力したExtension ID)が必須
const clovaMiddleware = clova.Middleware({applicationId: 'com.techtech.ubi'});
app.post('/clova', clovaMiddleware, clovaSkillHandler);
// app.get('/rpi', (req, res) => res.send('Hello Python'));

app.listen(port, () => console.log(`Server running on ${port}`));
