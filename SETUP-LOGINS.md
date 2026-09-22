# Switching on online saves (for a grown-up)

Mathcade saves progress in the browser, so it doesn't follow you to another computer.
Online saves fix that: you sign in with a Google account on the front page and your
progress is kept in a free Firebase database.

It's switched off until you do the steps below. Until then the site works exactly as
normal. It takes about 15 minutes.

## What you need

- A Google account (a parent's is fine).
- The site already **on the internet**. Google sign-in doesn't work on a page
  opened straight from a file on your computer (an address starting with
  `file://`). Do [PUT-IT-ONLINE.md](PUT-IT-ONLINE.md) first — it's the free
  GitHub Pages tutorial and takes about 20 minutes.

## 1. Make a Firebase project

1. Go to <https://console.firebase.google.com> and sign in.
2. Click **Create a project**. Call it `mathcade`. You can turn Google Analytics
   **off**, because it isn't needed.

## 2. Turn on Google sign-in

1. In the left menu: **Build → Authentication → Get started**.
2. On the **Sign-in method** tab, choose **Google**, switch it **on**, pick a
   support email, and click **Save**.

## 3. Make the database

1. In the left menu: **Build → Firestore Database → Create database**.
2. Pick a location near you. Start in **production mode**.
3. Open the **Rules** tab, replace everything there with the rules below, and
   click **Publish**. These rules mean each person can only read and write their
   own save:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /saves/{uid} {
      allow read, write: if request.auth != null && request.auth.uid == uid;
    }
  }
}
```

## 4. Get the settings for the website

1. Click the **gear icon → Project settings**.
2. Under **Your apps**, click the **web** icon (`</>`). Call it `mathcade`. You
   don't need Firebase Hosting ticked. Click **Register app**.
3. Firebase shows a block of code with `const firebaseConfig = { ... }` in it.
   Copy the part from `{` to `}`.

## 5. Paste the settings into Mathcade

1. Open `index.html` in a plain text editor (TextEdit in plain-text mode, VS Code
   or Notepad).
2. Search for `const FIREBASE_CONFIG = null;`
3. Replace `null` with what you copied. It should end up looking like this:

```js
const FIREBASE_CONFIG = {
  apiKey: "AIza...",
  authDomain: "mathcade-12345.firebaseapp.com",
  projectId: "mathcade-12345",
  storageBucket: "mathcade-12345.appspot.com",
  messagingSenderId: "1234567890",
  appId: "1:1234567890:web:abc123"
};
```

4. Save the file.

These settings aren't secret: every website that uses Firebase shows them. The
rules from step 3 are what keep each save private.

## 6. Put the site online (if you haven't yet)

Follow [PUT-IT-ONLINE.md](PUT-IT-ONLINE.md). You'll end up with an address like
`https://yourname.github.io/mathcade/`.

Whatever you use, remember to upload the changed files again whenever the games
change, and note the address for the next step.

## 7. Tell Firebase the site's address

1. In Firebase: **Build → Authentication → Settings → Authorized domains**.
2. Click **Add domain** and type the site's address without `https://` and
   without anything after the first slash, for example `yourname.github.io`.

## Done

Open the site. The profile card on the front page now has a **Save online** button.
Click it and sign in with Google. Do the same on any other computer to get the same
progress there.

## Good to know

- **The games still work offline.** Only the front page talks to Firebase. Progress
  from a game goes online the next time the front page is opened, which happens
  after every game anyway.
- **Two computers with different progress:** they're joined together, keeping the
  best of both. That means every star, win, trophy, car and record from either
  one. The save with more XP decides the things that can't be added up, like
  coins, the maths step and today's challenge.
- **Signing out** keeps the progress in that browser. It just stops syncing.
- **Start over** while signed in also wipes the online copy. That's on purpose:
  otherwise the old progress would be joined straight back in.
- **Cost:** a family using this stays far inside Firebase's free allowance.
