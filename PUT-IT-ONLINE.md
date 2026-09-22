# Putting Mathcade on the internet with GitHub

Right now Mathcade lives in a folder on this computer. This turns it into a real
website with an address you can send to anyone, like
`https://yourname.github.io/mathcade/`.

It's free. Do it with a grown-up, because making the account needs an email
address. It takes about 20 minutes the first time, and about 2 minutes every
time you want to put new changes online.

---

## Part 1 — Make a GitHub account

1. Go to <https://github.com> and click **Sign up**.
2. Put in an email address, make a password, and pick a username. The username
   becomes part of your website's address, so pick something you like, for
   example `chris-codes`.
3. GitHub emails you a code. Type it in.

---

## Part 2 — Make a place for the files (a "repository")

A repository, or **repo**, is just a folder that lives on GitHub.

1. Once you're signed in, click the **+** at the top right, then
   **New repository**.
2. **Repository name:** `mathcade`
3. Leave it as **Public**. (Public means anyone can play your games. It does
   *not* let anyone change them.)
4. Don't tick "Add a README file".
5. Click **Create repository**.

---

## Part 3 — Put your files in it

1. On the new repo's page, click the link that says **uploading an existing file**.
   (If you can't see it: **Add file → Upload files**.)
2. Open your `mathcade` folder on the computer. Select everything inside it:
   `index.html`, `mage-run.html`, `nitro-cup.html`, `tower-guard.html`,
   `prism-rush.html`, `striker-league.html`, and the `tools` folder.
3. Drag them onto the GitHub page.
4. Underneath, in the box that says "Commit changes", type what you did, like
   `First upload`.
5. Click **Commit changes** and wait for the files to finish uploading.

---

## Part 4 — Switch the website on (GitHub Pages)

1. In your repo, click **Settings** (the tab along the top).
2. In the left menu, click **Pages**.
3. Under **Build and deployment → Source**, pick **Deploy from a branch**.
4. Under **Branch**, pick **main**, leave the folder as **/ (root)**, and click
   **Save**.
5. Wait a minute or two, then refresh the page. It shows your address, something
   like `https://chris-codes.github.io/mathcade/`.

Open it. That's Mathcade, on the internet. It works on phones and tablets too:
send yourself the link.

> **If you get a 404 page:** wait another minute and refresh. Also check that
> `index.html` is directly inside the repo, not inside another folder.

---

## Part 5 — Changing your games later

Whenever the games change on this computer:

1. Go to your repo on GitHub.
2. Click **Add file → Upload files**.
3. Drag in the files that changed (or all of them again — that's fine).
4. Type what you changed, like `New Tower Guard towers`, and click
   **Commit changes**.
5. Wait about a minute. Refresh your website.

> **Tip:** if the page still looks old, hold **Shift** and press the reload
> button. That makes the browser fetch the new files instead of the ones it
> remembered.

---

## Is my progress safe?

Your stars, trophies and cash are saved **in your browser**, not in the files.
So:

- Putting the site online doesn't wipe anything.
- The online version starts empty, because it's a different address from the
  files on your computer.
- To have the same progress everywhere, switch on online saves. See
  [SETUP-LOGINS.md](SETUP-LOGINS.md) — and you need this GitHub step first,
  because Google sign-in doesn't work on files opened from your own computer.

---

## Words people use

| Word | What it means |
|---|---|
| Repository (repo) | A folder of your files on GitHub |
| Commit | Saving a change, with a note about what you did |
| Branch | A version of your files. Yours is called `main` |
| GitHub Pages | The free service that turns your repo into a website |
| 404 | "I can't find that page" |
