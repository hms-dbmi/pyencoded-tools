import encodedcc


def files(objList, fileCheckedItems, connection):
    for obj in objList:
        exp = encodedcc.get_ENCODE(obj, connection)
        if any(exp.get("files")):
            expfiles = exp["files"]
        else:
            expfiles = exp["original_files"]

        for f in expfiles:
            fileob = {}
            file = encodedcc.get_ENCODE(f, connection)
            for field in fileCheckedItems:
                fileob[field] = file.get(field)
            fileob["submitted_by"] = encodedcc.get_ENCODE(file["submitted_by"], connection)["title"]
            fileob["experiment"] = exp["accession"]
            fileob["experiment-lab"] = encodedcc.get(exp["lab"], connection)["name"]
            fileob["biosample"] = exp.get("biosample_term_name", "")
            fileob["flowcell"] = []
            fileob["lane"] = []
            fileob["Uniquely mapped reads number"] = ""

            if file.get("file_format", "") == "bam":
                for q in file.get("quality_metrics", []):
                    if "star-quality-metrics" in q.get("@id", ""):
                        fileob["Uniquely mapped reads number"] = q["Uniquely mapped reads number"]
            for fcd in file["flowcell_details"]:
                fileob["flowcell"].append(fcd.get("flowcell", ""))
                fileob["lane"].append(fcd["lane"])
            try:
                fileob["platform"] = encodedcc.get_ENCODE(fileob["platform"], connection)["title"]
            except:
                fileob["platform"] = None
            temp_rep = encodedcc.get_ENCODE(exp["replicates"][0], connection)
            temp_lib = encodedcc.get_ENCODE(temp_rep["library"], connection)
            temp_bio = encodedcc.get_ENCODE(temp_lib["biosample"], connection)
            temp_don = encodedcc.get_ENCODE(temp_bio["donor"], connection)
            temp_org = encodedcc.get_ENCODE(temp_don["organism"], connection)
            fileob = temp_org["name"]
            if "replicate" in file:
                rep = file["replicate"]
                





            if 'replicate' in file:
                    rep = file['replicate']
                    if 'library' in rep and rep['library'] is not None:
                        library = file['replicate'].get('library')
                        try:
                            fileob['library_aliases'] = library['aliases']
                        except:
                            fileob['library_aliases'] = ""
                        if 'biosample' in library:
                            fileob['biosample_aliases'] = library['biosample']['aliases']
            if 'alias' in exp:
                fileob['alias'] = exp['aliases'][0]
            else:
                fileob['alias'] = ''
            if 'replicate' in file:
                fileob['biological_replicate'] = file['replicate']['biological_replicate_number']
                fileob['technical_replicate'] = file['replicate']['technical_replicate_number']
                fileob['replicate_id'] = file['replicate'].get('uuid')
            else:
                fileob['biological_replicate'] = fileob['technical_replicate'] = fileob['replicate_alias'] = ''
            row = []
            for j in fileCheckedItems:
                row.append(repr(fileob[j]))
            print('\t'.join(row))
