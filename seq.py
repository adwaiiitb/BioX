import requests
import biotite.structure.io as bsio
import py3Dmol

def predict_structure(sequence: str, file_name=input("File name in .pdb format: ")):

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(
        "https://api.esmatlas.com/foldSequence/v1/pdb/",
        headers=headers,
        data=sequence,
    )
    pdb_string = response.content.decode("utf-8")

    # PDB file
    with open(file_name, "a") as f:
        f.write(pdb_string)

    return pdb_string

def visualize_structure(pdb_string: str,out_html=input("Save your file name with .html in the end: ")):

    view = py3Dmol.view(width=800, height=600)
    view.addModel(pdb_string, "pdb")
    view.setBackgroundColor('black')
    view.setStyle({"cartoon": {"color": "spectrum"}})
    view.zoomTo()
    view.zoom(2, 800)
    view.spin(True)

    # Writing HTML file
    with open(out_html, "x") as f:
        f.write(view._make_html())

    print(f"Structure visualization saved to {out_html}")

if __name__ == "__main__":
    # Let user input sequence or fallback
    seq = input("Enter protein sequence: ").strip()
    if not seq:
       seq= input("Please enter the sequence: ").strip()

    print("Predicting structure... this may take some seconds.")
    pdb_string = predict_structure(seq)

    print("PDB file saved as predicted.pdb")

    visualize_structure(pdb_string)
    print("Open 'structure.html' in your browser to see the 3D structure.")
