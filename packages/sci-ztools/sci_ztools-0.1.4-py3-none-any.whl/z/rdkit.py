from rdkit import Chem, DataStructs


def smi2fp(smi):
    try:
        m = Chem.MolFromSmiles(smi)
        fp = Chem.RDKFingerprint(m)
        return fp
    except Exception as e:
        print(e)
        return None


def get_similarity(fp1, fp2):
    return DataStructs.FingerprintSimilarity(fp1, fp2)
