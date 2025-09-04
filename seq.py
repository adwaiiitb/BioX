import requests
import biotite.structure.io as bsio
import py3Dmol

def predict_structure(sequence: str, file_name=input("file name in .pdb format")):
    """Send protein sequence to ESMFold API and return PDB string + mean plDDT."""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(
        "https://api.esmatlas.com/foldSequence/v1/pdb/",
        headers=headers,
        data=sequence,
    )
    pdb_string = response.content.decode("utf-8")

    # Save PDB file
    with open(file_name, "a") as f:
        f.write(pdb_string)

    # Compute mean plDDT (stored in b-factor)
    struct = bsio.load_structure(file_name, extra_fields=["b_factor"])
    b_value = round(struct.b_factor.mean(), 4)

    return pdb_string, b_value

def visualize_structure(pdb_string: str,out_html=input("Save your file name with .html in the end: ")):
    """Render protein structure with py3Dmol into an HTML file."""
    view = py3Dmol.view(width=800, height=600)
    view.addModel(pdb_string, "pdb")
    view.setBackgroundColor('black')
    view.setStyle({"cartoon": {"color": "spectrum"}})
    view.zoomTo()
    view.zoom(2, 800)
    view.spin(True)
    # Write HTML file
    with open(out_html, "x") as f:
        f.write(view._make_html())
    print(f"Structure visualization saved to {out_html}")

if __name__ == "__main__":
    # Let user input sequence or fallback
    seq = input("Enter protein sequence: ").strip()
    if not seq:
       seq= input("Please enter the sequence.").strip()

    print("Predicting structure... this may take some seconds.")
    pdb_string, mean_plddt = predict_structure(seq)

    print("PDB file saved as predicted.pdb")

    visualize_structure(pdb_string)
    print("Open 'structure.html' in your browser to see the 3D structure.")
