# Handbook Git Dasar

Dokumen ini merangkum materi Git yang telah dipelajari.

## 1. `git init`
Membuat repository Git baru.

```bash
git init
```

---

## 2. `git remote add origin`
Menghubungkan repository lokal ke GitHub.

```bash
git remote add origin https://github.com/username/repository.git
git remote -v
```

---

## 3. `git status`
Melihat status repository.

```bash
git status
```

Menampilkan:
- Branch aktif
- File yang berubah
- File baru
- Status sinkronisasi dengan GitHub

---

## 4. `git diff`
Melihat perubahan dibanding commit terakhir.

```bash
git diff
```

---

## 5. `git add`
Menambahkan perubahan ke Staging Area.

```bash
git add <file>
git add .
```

---

## 6. `git commit`
Menyimpan snapshot perubahan.

```bash
git commit -m "Pesan commit"
```

---

## 7. `git log`
Melihat riwayat commit.

```bash
git log --oneline
git log --oneline --graph
git log --oneline --graph --all
git log --oneline --graph --decorate --all
```

---

## 8. `git reflog`
Melihat riwayat aktivitas Git.

```bash
git reflog
```

---

## 9. `git switch -c`
Membuat branch baru.

```bash
git switch -c feature/nama-fitur
```

---

## 10. `git switch`
Berpindah branch.

```bash
git switch main
```

---

## 11. `git branch`
Melihat daftar branch.

```bash
git branch
```

---

## 12. `git merge`
Menggabungkan branch ke branch aktif.

```bash
git merge feature/nama-fitur
```

---

## 13. `git branch -d`
Menghapus branch yang sudah selesai.

```bash
git branch -d feature/nama-fitur
```

---

## 14. `git push`
Mengirim commit ke GitHub.

```bash
git push
git push -u origin main
```

---

## 15. `git pull`
Mengambil perubahan terbaru dari GitHub.

```bash
git pull
```

---

# Konsep Penting

## Ahead
Repository lokal memiliki commit yang belum dikirim ke GitHub.

Solusi:

```bash
git push
```

## Behind
Repository lokal tertinggal dari GitHub.

Solusi:

```bash
git pull
```

## Merge Commit
Commit khusus yang menggabungkan dua riwayat branch menjadi satu.

---

# Alur Kerja Git

```text
Working Directory
      │
   git add
      ▼
Staging Area
      │
 git commit
      ▼
Repository Lokal
      │
  git push
      ▼
GitHub
```

---

# Workflow yang Sudah Dipelajari

```text
git init
    │
git add
    │
git commit
    │
git push
    │
Buat Branch
    │
Coding
    │
git add
    │
git commit
    │
git switch main
    │
git merge feature/...
    │
git branch -d feature/...
    │
git push
```

---

# Roadmap Selanjutnya

- Merge Conflict
- Pull Request
- `.gitignore`
- `git stash`
- `git reset`
- `git revert`
- `git rebase`
- `git cherry-pick`
- Git Tags
