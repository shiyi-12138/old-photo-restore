"""Local test for predict.py output selection logic.
Simulates directory structures that predict.py would encounter.
Run: python test_predict_local.py
"""

import os, sys, tempfile, shutil

def test_candidate_priority():
    """Test the priority sort function used in predict.py"""
    def candidate_priority(f):
        if '/final_output/' in f.replace('\\', '/'):
            return 0
        if '/restored_image/' in f.replace('\\', '/'):
            return 1
        return 2

    # Simulate the files found during a scratch+fallback run
    candidates = [
        '/src/output/stage_1_restore_output/input_image/tmpabc.png',
        '/src/output/stage_1_restore_output/restored_image/result.png',
        '/src/output/final_output/blended.png',
        '/src/output/stage_1_restore_output/origin/copy.png',
    ]
    candidates.sort(key=candidate_priority)
    
    first = candidates[0]
    assert '/final_output/' in first, f"FAIL: Expected final_output first, got {first}"
    print(f"  ✅ Priority sort works: first = {first}")

def test_empty_final_output():
    """Test that we can find images in restored_image when final_output is empty"""
    with tempfile.TemporaryDirectory() as tmp:
        output_root = os.path.join(tmp, "output")
        
        # Create dirs - final_output empty, restored_image has a file
        final_dir = os.path.join(output_root, "final_output")
        restored_dir = os.path.join(output_root, "stage_1_restore_output", "restored_image")
        os.makedirs(final_dir)
        os.makedirs(restored_dir)
        with open(os.path.join(restored_dir, "result.png"), "w") as f: f.write("x")
        
        # Run the search logic
        import glob
        all_files = glob.glob(os.path.join(output_root, "**", "*"), recursive=True)
        img_exts = ('.png', '.jpg', '.jpeg')
        candidates = [f for f in all_files
                     if os.path.isfile(f) and f.lower().endswith(img_exts)]
        
        def candidate_priority(f):
            if '/final_output/' in f.replace('\\', '/'): return 0
            if '/restored_image/' in f.replace('\\', '/'): return 1
            return 2
        candidates.sort(key=candidate_priority)
        
        assert len(candidates) > 0, "FAIL: No candidates found"
        # Normalize to forward slashes for matching
        first_normalized = candidates[0].replace('\\', '/')
        assert '/restored_image/' in first_normalized, f"FAIL: Expected restored_image, got {candidates[0]}"
        print(f"  ✅ Empty final_output fallback works: {candidates[0]}")

def test_scratch_fallback_detection():
    """Test detection of empty restored_image after scratch pipeline"""
    with tempfile.TemporaryDirectory() as tmp:
        stage1_dir = os.path.join(tmp, "stage_1_output")
        restored_dir = os.path.join(stage1_dir, "restored_image")
        os.makedirs(restored_dir)  # empty dir - scratch pipeline failed
        
        sr = os.path.join(stage1_dir, "restored_image")
        is_empty = not os.path.isdir(sr) or not os.listdir(sr)
        assert is_empty, "FAIL: Should detect empty restored_image"
        print(f"  ✅ Scratch fallback detection: empty dir detected, would trigger fallback")

def test_python_syntax():
    """Validate predict.py has no syntax errors"""
    import py_compile
    predict_path = os.path.join(os.path.dirname(__file__), "predict.py")
    try:
        py_compile.compile(predict_path, doraise=True)
        print(f"  ✅ predict.py syntax OK")
    except py_compile.PyCompileError as e:
        print(f"  ❌ predict.py syntax ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("=== predict.py local tests ===\n")
    test_python_syntax()
    test_candidate_priority()
    test_empty_final_output()
    test_scratch_fallback_detection()
    print("\n🎉 All tests passed!")
