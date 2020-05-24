const sendPushNotification = (message) => {
	return new Promise( async (resolve, reject) => {
    var apn = require('apn');

    var options = {
      token: {
        key: "*.p8",
        keyId: "*",
        teamId: "*",
      },
      cert: "*.pem",
      key: "*.pem",
      production: true
    };

    var apnProvider = new apn.Provider(options);

    let deviceTokens = []

    var note = new apn.Notification();

    note.expiry = Math.floor(Date.now() / 1000) + 3600; // Expires 1 hour from now.
    note.badge = 0;
    note.sound = "ping.aiff";
    note.alert = message
    note.topic = "com.*.*";

    apnProvider.send(note, deviceTokens).then( (result) => {
      console.log(result)
      resolve(result)
    });
})
}

exports.sendPushNotification = sendPushNotification;