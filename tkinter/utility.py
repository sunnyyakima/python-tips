
# utility funcitons

import re
import xlwt

Header_Nof1          = "sequencing-type-xml\tgene-xml\tmap-location-xml\ttranscript-id-xml\tcoding-seq-change-xml\tvariant-location-report\tprotein-change-xml\tvariant-name-full-report\tvariant-type-xml\tcomment-xml\tsequencing-method-xml\tplatform-xml\tresult-xml\tcopy-number-xml\tcopy-number-change-xml\tMolecular consequence"
Header_Additional    = "Allele_Freq_Global_Minor\tAlt_Variant_Freq\tRead_Depth\tReference_nucleotide\tObserved_nucleotide\tReference_Amino_Acid\tObserved_Amino_Acid\tProtein_Start_Position\tProtein_Stop_Position\tApproximate_genomic_start_position\tGenome_build\tGenomic_Source\tTranscript_ID\tsource(NCBI)\tHGVS_genomic_change"
## note that "YES1" doesn't have transcript and "CDKN2A" has two transcripts
Preferred_transcript = ("NM_001014432","NM_004304","NM_000051","NM_004333","NM_007294","NM_000059","NM_053056","NM_000075","NM_001259","NM_000077","NM_058195","NM_005211","NM_005228","NM_004431","NM_004448","NM_023110","NM_000141","NM_000142","NM_002019","NM_004119","NM_002020","NM_002037","NM_005270","NM_002253","NM_000222","NM_004985","NM_005356","NM_002350","NM_002755","NM_002755","NM_030662","NM_002447","NM_004958","NM_002524","NM_006206","NM_002609","NM_000264","NM_002880","NM_000321","NM_020975","NM_002944","NM_005631","NM_005417","NM_000368","NM_000548","NM_000551","NM_001904","NM_005235","NM_002392","NM_017617","NM_006218","NM_005359","NM_000455","NM_000546","NM_000038","NM_001654","NM_001204106","NM_001014796","NM_002067","NM_002072","NM_001527","NM_005343","NM_000875","NM_004972","NM_000215","NM_001127500","NM_000249","NM_000251","NM_000179","NM_000535","NM_002691","NM_006231","NM_000314","NM_023067","NM_000516","NM_198253","NM_001122742","NM_000061","NM_006180","NM_000459","NM_005433")
Conseq_kept          = ("coding_sequence_variant","feature_truncation","frameshift_variant","incomplete_terminal_codon_variant","inframe_deletion","inframe_insertion","missense_variant","protein_altering_variant","splice_acceptor_variant","splice_donor_variant","splice_region_variant","start_lost","stop_gained","stop_lost","stop_retained_variant","transcript_truncation","feature_elongation","transcript_ablation")
KnownVariants        = ("NM_000142.4:c.445+3A>G","NM_006231.2:c.4290+5C>T","NM_000535.5:c.2006+6G>A","NM_000077.4:c.442G>A","NM_002447.2:c.965G>A","NM_000059.3:c.2971A>G","NM_006206.4:c.368-3C>T","NM_000535.5:c.1454C>A","NM_005235.2:c.2965-7_2965-4delCTTT","NM_000141.4:c.557T>C","NM_006231.2:c.4444+4T>A","NM_007294.3:c.1067A>G","NM_006218.2:c.1173A>G","NM_000535.5:c.59G>A","NM_002072.3:c.286A>T","NM_023067.3:c.536C>G","NM_000051.3:c.5557G>A","NM_000368.4:c.965T>C","NM_006180.3:c.1765-7T>C","NM_005631.4:c.74A>G","NM_000368.4:c.3127_3129delAGC","NM_002944.2:c.500G>A","NM_002944.2:c.3326C>T","NM_002944.2:c.5941-4A>G","NM_000535.5:c.2007-7C>T","NM_000368.4:c.1335A>G","NM_000251.2:c.2006-6T>C","NM_002020.4:c.1480A>G","NM_006231.2:c.4187A>G","NM_002755.3:c.1023-8C>T","NM_005211.3:c.1085A>G","NM_002691.3:c.463+8G>T","NM_006231.2:c.755C>T","NM_002691.3:c.356G>A","NM_006206.4:c.1432T>C","NM_002020.4:c.3437G>A","NM_000535.5:c.2007-4G>A","NM_004304.4:c.4165-6C>T","NM_020975.4:c.2071G>A","NM_002020.4:c.445A>G","NM_005631.4:c.67_69delCTG","NM_002944.2:c.433A>C","NM_030662.3:c.453C>T","NM_002944.2:c.6686C>G","NM_002944.2:c.6682A>C","NM_002944.2:c.6637G>A","NM_000455.4:c.920+7G>C","NM_000535.5:c.2570G>C","NM_000059.3:c.1114A>C","NM_000249.3:c.655A>G","NM_004448.2:c.1963A>G","NM_000179.2:c.116G>A","NM_004304.4:c.3359+6C>T","NM_004304.4:c.4472A>G","NM_007294.3:c.3113A>G","NM_007294.3:c.4837A>G","NM_007294.3:c.3548A>G","NM_005228.3:c.1562G>A","NM_000535.5:c.1408C>T","NM_004119.2:c.20A>G","NM_007294.3:c.2612C>T","NM_000264.3:c.3944C>T","NM_002609.3:c.3137+4A>G","NM_017617.3:c.2588-4G>A","NM_002447.2:c.4003A>G","NM_002447.2:c.1568A>G","NM_004304.4:c.4587C>G","NM_053056.2:c.723G>A","NM_002944.2:c.3855-5T>C","NM_004448.2:c.3508C>G","NM_005270.4:c.3466G>T","NM_017617.3:c.1441+7C>T","NM_004119.2:c.680C>T","NM_005270.4:c.3916G>A","NM_002020.4:c.2670C>G","NM_004119.2:c.1310-3T>C","NM_000038.5:c.5465T>A","NM_000546.5:c.215C>G","NM_000535.5:c.1621A>G","NM_000459.3:c.1037A>C","NM_000059.3:c.7397T>C","NM_004304.4:c.4381A>G","NM_002447.2:c.3583A>G","NM_002253.2:c.889G>A")
Quality_threshold    = 95
Read_depth           = 65


def parseIn(inf):      # parse the outfile from variantstudio; THE ORDER OF COLUMN IS FIXED
    data_Hash = {}     # output is a hash, the value is a list
    file_in = open(inf, "r")
    contents = file_in.read()
    list_of_lines = [line.split('\t') for line in contents.split('\n')]
    for i in range(len(list_of_lines)):
        if(re.search(",", list_of_lines[i][0])):         # skip the case that have two gene ID(gene1,gene2)
            continue
        if (list_of_lines[i][0] != '') :
            list_of_lines[i] = dealWsplice(list_of_lines[i])
            data_Hash["variant_"+str(i)] = list_of_lines[i]
    return data_Hash


def dealWsplice(inVar):  # inVar: Gene, Variant, Chr, Coordinate, Consequence, HGVSc, HGVSp, Classification
    if(inVar[6] == "" and re.search("splice", inVar[4])):
        site = getChange(inVar[5])
        inVar[6] = inVar[0]+":splice_site_"+str(site)
    return inVar

def filter_qual(inHash, Quality=Quality_threshold, Reads=Read_depth):    # filter based on 1: quality, frequency, consequence and preferred transcripts(NOTE: YES1) 
    out_Hash = {}
    for k in inHash.keys():
        if(inHash[k][5] == ""):
            continue
#        print("==>"+k +"<==\t" + "=>"+inHash[k][11]+"<=\t"+"=>"+inHash[k][12]+"<=\t=>"+inHash[k][16]+"=><=")
        
        if(inHash[k][11] == "PASS" and int(inHash[k][12]) >= Quality and int(inHash[k][16]) >= Reads and check_conseq(inHash[k][4])): # and getID(inHash[k][5]) in Preferred_transcript):
            out_Hash[k] = inHash[k]
    return out_Hash

def filter_qual2(inHash):  # keep coding-changing mutation for non-preferred transcripts
    out_Hash = {}
    flag = {}
    for k in inHash.keys():
        if(getID(inHash[k][5]) in Preferred_transcript):
            flag[str(inHash[k][2]) +"_"+ str(inHash[k][3])] = 1
    for k in inHash.keys():
        if(getID(inHash[k][5]) in Preferred_transcript):
            out_Hash[k] = inHash[k]
        elif(not  str(inHash[k][2]) +"_"+ str(inHash[k][3]) in flag and re.search("^NM_", inHash[k][5])):
            out_Hash[k] = inHash[k]
            flag[str(inHash[k][2]) +"_"+ str(inHash[k][3])] = 1
    return out_Hash

def filter_knowns(inHash):
    outHash = {}
    for k in inHash.keys():
        if(inHash[k][5] not in KnownVariants):
            outHash[k] = inHash[k]
    return outHash


def check_conseq(conseq):  # Conseq may have > 1 elems, return a Boolean
    if(re.search(",", conseq)):
        elems = conseq.split(",")
        for elem in elems:
            if(elem in Conseq_kept):
                return 1
        return 0
    elif(conseq in Conseq_kept):
        return 1
    return 0
    
def getChange(inStr):  # parse HGVSc/HGVSp, get ID and change
#    print(inStr)
    (ID,  change0) = inStr.split(":")
    change1 = re.sub(r"^c.", "", change0)
    change  = re.sub(r"^p.", "", change1)
    return change

def getID(inStr):
    (ID0, change) = inStr.split(":")
    (ID, version) = ID0.split(".")
    return ID

def printHeader_varStu(Hash_data):  # print out the header to shell
    for k in Hash_data:
        if(Hash_data[k][0] == "Gene"):
            print(Hash_data[k])
            exit()
    print("There is NO header info\n")

def convert2N_of_1(inData): # inData is a Hash of list after filtering
    outData = {}            #: 'Gene', 'Variant', 'Chr', 'Coordinate', 'Consequence', 'HGVSc', 'HGVSp', 'Allele Freq Global Minor(AFGM)', 'Alt Variant Freq', 'Read Depth'
    for k in inData:        #:    0        1        2         3              4           5        6       39                                15                  16 
        if(inData[k][0] == "Gene" or inData[k][0] == ""):
            continue
        gene              = inData[k][0]
        sequence_method   = "sequencing"
        coding_seq_change = getChange(inData[k][5])
     #   print("protein:  ===>" + inData[k][6] + "<===")
        if(inData[k][6] == ""):
            protein_change = ""
        else:
            protein_change = getChange(inData[k][6])
         #   protein_change    = protein_change0.split(".")[1]
        map_location      = "chr"+str(inData[k][2]) + ":" + str(inData[k][3])
        transcriptID      = getID(inData[k][5])
        variantType       = "short-variant"
        comment           = ""
        platform          = "miSeq"
        result            = "positive"
        full_Name         = str(gene)+"_"+ protein_change #  str(getChange(inData[k][6]))
        var_location      = inData[k][5]
        copyNum           = ""
        copyNumChange     = ""
        MolConseq         = inData[k][4]
        AFGM              = str(inData[k][39])
        AltVariantFreq    = str(inData[k][15])
        ReadDepth         = str(inData[k][16])
        outData[k]=sequence_method+"\t"+gene+"\t"+map_location+"\t"+transcriptID+"\t"+coding_seq_change+"\t"+var_location+"\t"+protein_change+"\t"+full_Name+"\t"+variantType+"\t"+comment+"\tseq\t"+platform+"\t"+result+"\t"+copyNum+"\t"+copyNumChange+"\t"+MolConseq+"\t"+AFGM+"\t"+AltVariantFreq+"\t"+ReadDepth

    return outData

def convert2N_of_1_v1(inData): # inData is a Hash of list after filtering
    outData = {}            #: 'Gene', 'Variant', 'Chr', 'Coordinate', 'Consequence', 'HGVSc', 'HGVSp', 'Allele Freq Global Minor(AFGM)', 'Alt Variant Freq', 'Read Depth'
    for k in inData:        #:    0        1        2         3              4           5        6       39                                15                  16

                            # FLAG	FilesPresent	Gene_0	Variant_1	Chr_2	Coordinate_3	Quality_9	Alt Variant Freq_13	Read Depth_14	Alt Read Depth_15	Consequence_28	Protein Position_31	Amino Acids_32	Sift_39	PolyPhen_40	HGVSc_42	HGVSp_43	dbSNP ID_44	Ancestral Allele_45	Allele Freq_46	COSMIC ID_57	COSMIC Primary Site_61	ClinVar RS_63	ClinVar Disease Name_68	ClinVar MedGen_70	ClinVar OMIM_71	ClinVar Orphanet_72	ClinVar GeneReviews_73	ClinVar SnoMedCt ID_74	StrandBias	IGV_Link

        if(inData[k][0] == "FLAG" or inData[k][0] == ""):
            continue
        gene              = inData[k][2]
        sequence_method   = "sequencing"
        coding_seq_change = getChange(inData[k][15])
        if(inData[k][16] == "" or inData[k][16] == " "):
            protein_change = ""
        else:
            protein_change = getChange(inData[k][16])
        map_location      = "chr"+str(inData[k][4]) + ":" + str(inData[k][5])
        transcriptID      = getID(inData[k][15])
        variantType       = "short-variant"
        comment           = ""
        platform          = "miSeq"
        result            = "positive"
        full_Name         = str(gene)+"_"+ protein_change #  str(getChange(inData[k][6]))
        var_location      = inData[k][15]
        copyNum           = ""
        copyNumChange     = ""
        MolConseq         = inData[k][10]
        AFGM              = "0"
        AltVariantFreq    = str(inData[k][7])
        ReadDepth         = str(inData[k][8])
        outData[k]=sequence_method+"\t"+gene+"\t"+map_location+"\t"+transcriptID+"\t"+coding_seq_change+"\t"+var_location+"\t"+protein_change+"\t"+full_Name+"\t"+variantType+"\t"+comment+"\tseq\t"+platform+"\t"+result+"\t"+copyNum+"\t"+copyNumChange+"\t"+MolConseq+"\t"+AFGM+"\t"+AltVariantFreq+"\t"+ReadDepth

    return outData


def write2file(outfile, header, data):
    outf = open(outfile, "w")
    outf.write(header + "\n") #Header_Nof1 + "\t" + Header_Additional + "\n")

    for k in sorted(data):
        outf.write(data[k] + "\n")

    outf.close()

def write2excel(outfile, header, data):
    book = xlwt.Workbook()
    sheet1 = book.add_sheet("NofOne")
    headers = header.split("\t")
    for column, heading in enumerate(headers):
        sheet1.write(0, column, heading)
    i = 1
    for k in sorted(data):
        d = data[k].split("\t")
        for col, cell in enumerate(d):
            if(d[3] not in Preferred_transcript):
                st = xlwt.easyxf('pattern: pattern solid;')
                st.pattern.pattern_fore_colour = xlwt.Style.colour_map['light_yellow']
                sheet1.write(i, col, cell, st)
            else:
                sheet1.write(i, col, cell)
        i = i + 1
    book.save(outfile + ".xls")


'''
#file = "C:\\Users\\yliu\\Project_UI\\convert2NofONE_0.1\\6_tube6_S6.tsv"
in_data0 = parseIn("VarDict_run170131_4T16-000315FM_S4.tsv")

in_data1 = filter_qual(in_data0)
print(in_data1)
exit()
out_data = convert2N_of_1(in_data1)
print(out_data)
'''

