import os
import pytest
import file_manager as fm

def test_get_size():
    assert fm.getSize(500000) == "0.48 MB"
    assert fm.getSize(1048576) == "1.00 MB"
    assert fm.getSize(1500000) == "1.43 MB"
    assert fm.getSize(1073741824) == "1.00 GB"
    assert fm.getSize(2500000000) == "2.33 GB"

def test_get_cat():
    assert fm.get_cat(".jpg") == "Images"
    assert fm.get_cat(".JPG") == "Images"
    assert fm.get_cat(".pdf") == "Documents"
    assert fm.get_cat(".exe") == "Executables"
    assert fm.get_cat(".xyz") == "Others"
    assert fm.get_cat("") == "Others"

def test_calc_folder_size(tmp_path):
    f1 = tmp_path / "file1.txt"
    f1.write_bytes(b"x" * 1024)

    sub = tmp_path / "subfolder"
    sub.mkdir()
    f2 = sub / "file2.txt"
    f2.write_bytes(b"x" * 2048)

    total = fm.calc_folder_size(str(tmp_path))
    assert total == 3072

def test_calc_folder_size_empty(tmp_path):
    assert fm.calc_folder_size(str(tmp_path)) == 0

def test_organize_basic_moves(tmp_path):
    (tmp_path / "pic.jpg").write_text("image data")
    (tmp_path / "report.pdf").write_text("doc data")
    (tmp_path / "script.py").write_text("print('hi')")
    (tmp_path / "random.dat").write_text("???")

    fm.organize(str(tmp_path))

    assert (tmp_path / "Images" / "pic.jpg").exists()
    assert (tmp_path / "Documents" / "report.pdf").exists()
    assert (tmp_path / "Code" / "script.py").exists()
    assert (tmp_path / "Others" / "random.dat").exists()

    assert not (tmp_path / "pic.jpg").exists()
    assert not (tmp_path / "report.pdf").exists()

def test_organize_ignores_folders(tmp_path):
    sub = tmp_path / "Images"
    sub.mkdir()
    (sub / "should_not_move.jpg").write_text("data")

    fm.organize(str(tmp_path))

    assert (tmp_path / "Images" / "should_not_move.jpg").exists()

def test_organize_handles_duplicates(tmp_path):
    target_dir = tmp_path / "Images"
    target_dir.mkdir()
    (target_dir / "photo.jpg").write_text("original")

    (tmp_path / "photo.jpg").write_text("duplicate")
    (tmp_path / "photo_1.jpg").write_text("another duplicate")

    fm.organize(str(tmp_path))

    assert (target_dir / "photo.jpg").read_text() == "original"
    assert (target_dir / "photo_1.jpg").read_text() == "another duplicate"
    assert (target_dir / "photo_2.jpg").read_text() == "duplicate"

    assert not (tmp_path / "photo.jpg").exists()

def test_organize_skips_no_extension(tmp_path):
    f = tmp_path / "no_extension_file"
    f.write_text("data")

    fm.organize(str(tmp_path))

    assert f.exists()
    assert not (tmp_path / "Others" / "no_extension_file").exists()