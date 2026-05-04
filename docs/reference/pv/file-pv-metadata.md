### **`type`**

**Formal Name: `caDSR CDE 11416926 v1.00`** ([Link](https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=11416926%20and%20ver_nr=1))

This metadata element is defined by the caDSR as "A defined organization or layout representing and structuring data in a computer file.".

| Permissible Value | Description | VM Long Name | VM Public ID | Concept Code | Begin Date |
|:-- | -- | -- | -- | -- | -- |
| `ADF` | A tab-delimited file defining how each array in an investigation is used. This data includes what sequence is located at each position in an array and what the annotation of this sequence is; cross-references to entries in a public repository can be used if available. | Array Design Format | 11421996 | C172213 | 10/12/2022 |
| `AVI` | A multimedia container format for audio video interleaved (AVI) files that allows for synchronous audio-with-video playback. | AVI Format | 11421997 | C190162 | 10/12/2022 |
| `BAI` | An index file found in the same directory as the binary alignment map (BAM) file, a compressed binary version of a sequence alignment/map (SAM) file. | BAI File | 11421998 | C190163 | 10/12/2022 |
| `BAM` | A binary representation of a sequence alignment map (SAM), a compact and indexable representation of nucleotide sequence alignments, compressed by the BGZF (Blocked GNU Zip Format) library. | Binary Alignment Map | 6356231 | C153249 | 10/12/2022 |
| `BCR Biotab` | Files that consist of aggregate clinical and biospecimen data across all cases of the given project. Biotab files are supplemental files that are available in the Genomic Data Commons (GDC) Legacy Archive as tab-delimited files on a project level basis. These may also include fields that are not available in the GDC application programming interface (API). | BCR Biotab Format | 11421999 | C190164 | 10/12/2022 |
| `BED` | A tab-delimited text file format that allows the specification of the sequence data that is displayed in an annotation track. The minimum required information is chromosome, start position, and end position. | BED Format | 11422000 | C153367 | 10/12/2022 |
| `bedgraph` | A format that allows display of continuous-valued data in track format. This display type is useful for probability scores and transcriptome data. | Bedgraph Format | 11422001 | C190165 | 10/12/2022 |
| `BEDPE Format` | A text file format used to store genomic paired-end sequencing data that includes coordinates and associated metadata. | BEDPE Format | 14535229 | C184749 | 10/16/2023 |
| `bigBed` | A format for large sequence annotation tracks, similar to the textual browser extensible data (BED) format. The annotated items can be either simple or a linked collection of exons. | BigBed Format | 11422002 | C190166 | 10/12/2022 |
| `bigWig` | A format for large sequence annotation tracks that consist of a value for each sequence position, similar to the textual wiggle (WIG) format. | BigWig Format | 11422003 | C190167 | 10/12/2022 |
| `Binary Format` | A file format in which file information is stored in the form of ones and zeros. It can be easily converted to text representations for visualization and editing. | Binary Format | 11422004 | C190168 | 10/12/2022 |
| `BIOM` | A general-use format for representing biological sample by observation contingency tables. It is designed for general use in broad areas of comparative -omics. The primary use of this format is to represent operational taxonomic unit (OTU) and metagenome tables. | BIOM Format | 11422059 | C190169 | 10/12/2022 |
| `cdf` | A file that provides information about the probes contained within an Affymetrix expression microarray probe set. | Affymetrix Probe Sets Library File | 15354255 | C209894 | 12/02/2024 |
| `CEL` | A type of file that stores the results of intensity calculations of pixel values for DNA microarray image analysis. The data includes an intensity value, standard deviation of the intensity, the number of pixels used to calculate the intensity value, a flag to indicate an outlier as calculated by the algorithm, and a user defined flag indicating whether the feature should be excluded from future analysis. The file also stores the previously stated data for each feature on the probe array. | Affymetrix CEL Format | 12135194 | C191737 | 12/12/2022 |
| `CNS` | A gene expression report format that utilizes a graph with genes, proteins, and molecules represented as node and their interactions represented as links. | Cytoscape Input File Format | 15354253 | C209889 | 12/02/2024 |
| `CRAI` | An external index file created by the sequencing data archive alongside a compressed reference-oriented alignment map (CRAM) file. This index file is available in the same directory as the CRAM file and is required for selective access to the genomic sequence alignment data within the CRAM file. | CRAI File | 12517496 | C192224 | 02/01/2023 |
| `CRAM` | A more highly compressed alternative to the BAM and SAM DNA sequence alignment file formats. It uses reference based compression, with only base calls that differ from a designated reference sequence being stored. | CRAM Format | 11422061 | C190170 | 10/12/2022 |
| `CSV` | A text file format that separates data elements with commas. | Comma Separated Values Format | 7797849 | C182456 | 10/12/2022 |
| `DICOM` | A comprehensive set of standards for communications between medical imaging devices, including handling, storing and transmitting information in medical imaging. It includes a file format definition and a network communication protocol. | DICOM | 2967848 | C49059 | 10/12/2022 |
| `DICT` | The simple flat file format of an entry from the HET group dictionary, a PDB file resource for ligand groups that are found complexed to protein structures. | HET Group Dictionary Entry Format | 15354254 | C209890 | 12/02/2024 |
| `DOC` | A Microsoft proprietary Binary Interchange file format used for word processing documents. It was replaced with DOCX format in 2007. | DOC Format | 15354330 | C210442 | 12/02/2024 |
| `DOCX` | A file type that uses Open XML Document format to store data for Microsoft Word and other compatible programs. | DOCX Format | 11422062 | C190171 | 10/12/2022 |
| `DSV` | A delimiter-separated values file that contains plain text data divided into rows and columns by a designated special character. | DSV Format | 11422063 | C190172 | 10/12/2022 |
| `FASTA` | A sequence in FASTA format consists of a single-line description, followed by lines of sequence data. The first character of the description line is a greater-than (">") symbol in the first column. Sequences are represented in the standard IUB/IUPAC single letter amino acid and nucleic acid codes, with a single hyphen or dash being used to represent a gap of indeterminate length; in amino acid sequences asterix ("*") can represent a translation stop. | FASTA Format | 11422064 | C47845 | 10/12/2022 |
| `FASTQ` | A a tab-delimited containing information about an investigation, including its name, a description, the investigator's contact details, bibliographic references, and free text descriptions of any relevant protocols. | Investigation Description Format | 11422065 | C172212 | 10/12/2022 |
| `GCT/Res Format` | A tab-delimited text file that contains gene expression data as a column for each sample, a row for each gene, and an expression value for each gene in each sample. RES differs from GCT by having labels for each gene's absent (A) versus present (P) calls as generated by Affymetrix's GeneChip software. | GCT/RES Format | 11422066 | C190173 | 10/12/2022 |
| `GenBank Format` | A type of flat file format that allows for the storage of DNA or protein sequences and annotations. It consists of an annotation section and a sequence section. | GenBank Format | 11422129 | C190174 | 10/12/2022 |
| `GFF3` | A tab-separated format for sequence data. It uses one line per feature, each containing 9 columns of data, plus optional track definition lines. | General Feature Format Version 3 | 11422130 | C190175 | 10/12/2022 |
| `GPR` | A tab-delimited text file format developed by Axon Instruments and used to export data from the microarray image analysis tool GenePix. | GenePix Results Format | 11422131 | C190176 | 10/12/2022 |
| `GTF` | A tab-delimited text format based on the general feature format (GFF) but which also contains some additional information for each gene. | GTF Format | 11422132 | C190177 | 10/12/2022 |
| `gVCF` | A text file format used for storing gene sequence variations. It is a type of variant call format that has a record for all sites, whether there is a variant call there or not. The format includes metrics of the confidence that positions are actually non-variant vs. a factor of minimum read-depth and genotype quality. | Genomic Variant Call Format | 14818706 | C204352 | 03/04/2024 |
| `GZIP Format` | A file format consisting of a 10-byte header containing a magic number, a version number, and a timestamp, a Deflate-compressed body, and an 8-byte footer containing a checksum and the length of the original uncompressed data. | Gzip File Format | 2929849 | C80220 | 10/12/2022 |
| `HDF5` | A hierarchical, filesystem-like data format that can store metadata in the form of user-defined, named attributes, which are attached to groups and datasets, and representations of images and tables built up using datasets, groups and attributes. | Hierarchical Data Format 5 | 11422133 | C184763 | 10/12/2022 |
| `HIC` | An indexed binary format designed to permit fast random access to contact matrix heatmaps. | HIC File Format | 14728934 | C203672 | 01/25/2024 |
| `HTML` | A standard markup language used to display content on a web page, as specified by the World Wide Web Consortium (W3C). | Hypertext Markup Language | 11422134 | C142380 | 10/12/2022 |
| `HTSeq Count` | A tab-delimited file generated by the HTSeq Count software tool. The file represents the number of reads obtained during high-throughput sequencing that map to known genomic sequences. The data is represented in two columns, one containing an identifier for a genomic feature, which can be a database-supplied identifier or a gene symbol, followed by a second column containing the number of mapped reads. | HTSeq-Count Output Format | 14943335 | C205749 | 05/23/2024 |
| `IDAT` | A proprietary, encrypted XML-based, compressed electronic file format from Illumina Inc. for storing genome-wide profiling data. The data contains a summary of the intensity data generated from each probe used during a sequencing run. | IDAT Format | 11495707 | C184762 | 10/26/2022 |
| `IDF` | A a tab-delimited containing information about an investigation, including its name, a description, the investigator's contact details, bibliographic references, and free text descriptions of any relevant protocols. | Investigation Description Format | 11422065 | C172212 | 10/26/2022 |
| `idpDB` | A self-contained file format that utilizes an open-source protein assembly tool to view and filter peptide-spectrum-matches, and stores relationships between proteins, peptides, and spectra. | IDPicker File Format | 15354267 | C209893 | 12/02/2024 |
| `JPEG` | A file compression format mostly used for color and greyscale photographs. | JPEG | 11422138 | C48230 | 10/26/2022 |
| `JPEG 2000` | A discrete wavelet transform (DWT)-based compression standard electronic file format for storing video images. | JPEG 2000 Format | 11422135 | C184768 | 10/26/2022 |
| `JSON` | A common open standard file format and data interchange format that uses human-readable text consisting of attribute-value pairs and arrays to store and transmit data. | JSON Format | 11422136 | C184769 | 10/26/2022 |
| `MAF` | A tab-delimited text file containing mutation information aggregated from variant call files (VCF) across a project, trial or study. | Mutation Annotation Format | 11422137 | C172215 | 10/26/2022 |
| `MAGE-TAB` | A tab-delimited, spreadsheet-based format that can be used for annotating and communicating microarray data in a MIAME (Minimum Information About a Microarray Experiment) compliant fashion. | MAGE-TAB | 2953599 | C82937 | 10/12/2022 |
| `MAT` | A proprietary, binary data container format used by MATLAB software to store workspace variables. | MAT Format | 11422139 | C190178 | 10/12/2022 |
| `MATLAB Script` | A file that contains MATLAB commands and function calls. | MATLAB Script File | 11422140 | C190179 | 10/12/2022 |
| `MEX` | A minimal base ASCII file format to facilitate the exchange of data matrices. | MEX Format | 14532371 | C184778 | 10/13/2023 |
| `MPEG-4` | A multimedia file that is commonly used to store  video and audio data. | MP4 Format | 11422141 | C190180 | 10/12/2022 |
| `mtx` | A format for the storage of numerical or pattern matrices in a dense (array format) or sparse (coordinate format) representation. | mtx | 14534322 | C201789 | 10/16/2023 |
| `mzIdentML` | An exchange format for peptides and proteins identified from mass spectra. | mzIdentML | 14534321 | C201788 | 10/16/2023 |
| `mzML` | An open-source format for mass spectrometer output files that was designed to be utilized and adapted as advances in mass spectrometry technology proceed. This was standardized by the Human Proteome Organization (HUPO)-Proteomics Standards Initiative (PSI) Mass Spectrometry Standards (MSS) Working Group. | Mass Spectrometry Markup Language | 11422142 | C190181 | 10/12/2022 |
| `mzXML` | An XML based common file format for mass spectrometry data. | Mass Spectrometry Extensible Markup Language | 11422143 | C47924 | 10/12/2022 |
| `NIFTI Format` | An open file format used to store neuroscience and neuroradiology imaging data obtained by MRI. The raw image data in NIfTI is saved as a 3d image. | NIfTI Format | 11422144 | C190183 | 10/12/2022 |
| `OME-TIFF` | A tagged image file format (TIFF) image file format that contains an Open Microscopy Environment (OME) XML metadata block in the file header for storing microscopy information (pixels and metadata) using the OME Data Model. | Open Microscopy Environment Tagged Image File Format | 11422196 | C181618 | 10/12/2022 |
| `PDF` | An open file format created and controlled by Adobe Systems, for representing two-dimensional documents in a device independent and resolution independent fixed-layout document format. Each PDF file encapsulates a complete description of a 2D document that includes the text, fonts, images, and 2D vector graphics that compose the document. PDF files do not encode information that is specific to the application software, hardware, or operating system used to create or view the document. This feature ensures that a valid PDF will render exactly the same regardless of its origin or destination (but depending on font availability when fonts are not encapsulated in the file). | Portable Document Format | 2967828 | C63805 | 10/12/2022 |
| `PED` | A standard text format for sample pedigree information and storage of marker genotypes, disease status, and quantitative trait values. | Pedigree File Format | 15092262 | C209891 | 09/04/2024 |
| `Plain Text Data Format` | A data format consisting of readable textual material maintained as a sequential file. | Plain Text Data Format | 11422197 | C85873 | 10/12/2022 |
| `PNG` | An extensible file format for lossless data compression of images. | Portable Network Graphics | 11422198 | C85437 | 10/12/2022 |
| `Python Script Format` | A plain text file that stores python code. | Python Script Format | 11422199 | C190184 | 10/12/2022 |
| `R File Format` | A file format used for writing scripts in the R programming language for execution within the R software environment, typically for statistical computation and graphics. | R Format | 11422200 | C190186 | 10/12/2022 |
| `R Markdown` | A file format for making dynamic documents written in R. It is written in plain text format and contains chunks of embedded R code. | R Markdown Format | 11422201 | C190187 | 10/12/2022 |
| `rds` | A binary file format that provides a method for saving R data sets and other objects. | Reference Data Set File Format | 15354268 | C209895 | 12/02/2024 |
| `RTF` | A file format that contains various formatting elements and enables exchanges of text files across different word processing platforms and applications. | Rich Text Format | 15092264 | C209896 | 09/04/2024 |
| `SDRF` | A tab-delimited file describing the relationships between samples, arrays, data and other objects used or produced during a microarray experiment. | Sample and Data Relationship Format | 11422202 | C172211 | 10/12/2022 |
| `SEG` | A tab-delimited text file that is the tabular output of the Circular Binary Segmentation algorithm implemented in DNAcopy and lists loci and associated numeric values. | Segmented Data Format | 15092263 | C209892 | 09/04/2024 |
| `Sequence Record Format` | Any file format designed to store molecular sequence data. | Sequence Record Format | 11422203 | C190188 | 10/12/2022 |
| `SVG` | A specification for describing vector graphics using extensible markup language. | Scalable Vector Graphics | 11422204 | C85435 | 10/12/2022 |
| `SVS` | An electronic file format based on TIFF that is used for storing multiple high-resolution images in a single electronic file. | Spectral View Settings Format | 11426797 | C172214 | 10/12/2022 |
| `TAR` | A file format generated by the Unix command-line utility tar (tape archive). It is used for collecting many files into one archive file. | TAR Format | 11426798 | C190189 | 10/12/2022 |
| `TBI` | A tab-delimited file that contains an index for the genome positions in a compressed (zipped) variant call format file. | TBI Format | 15042846 | C184806 | 08/19/2024 |
| `Thermo RAW` | A proprietary file format developed by Thermo Scientific to capture mass spectrometry data produced by Thermo mass spectrometers. | Thermo RAW Format | 11426799 | C190190 | 10/12/2022 |
| `TIFF` | A bitmap graphics file format utilizing tagged fields. | TIFF | 11426800 | C70631 | 10/12/2022 |
| `TSV` | A file format where each line in the file contains a single piece of data and where each field or value in a line of data is separated from the next by a tab character. | Tab-Separated Value Format | 11426801 | C164049 | 10/12/2022 |
| `TXT` | A data format consisting of readable textual material maintained as a sequential file. | Plain Text Data Format | 11422197 | C85873 | 10/12/2022 |
| `VCF` | A text-based electronic file used for storing gene sequence variation data. The first text section is composed of a header containing the metadata and keywords used in the file. This is followed by the body of the file which is tab-separated into eight mandatory data columns for each sample. Additionally, the body of the file can include an unlimited number of optional columns to record other sample-related data. | Variant Call File Format | 11426802 | C172216 | 10/12/2022 |
| `XLS` | A proprietary binary file format used to store spreadsheet data in Microsoft Excel. | XLS Format | 11426803 | C190191 | 10/12/2022 |
| `XLSX` | A proprietary file format developed by Microsoft that allows the user to save a spreadsheet created in Excel in an open XML-format. The file then can be read and opened by other spreadsheet-compatible applications. | Excel Open XML Format | 11426804 | C164050 | 10/12/2022 |
| `XML` | Extensible Markup Language | Extensible Markup Language | 2581637 | C45967 | 10/12/2022 |
| `YAML` | A human-readable, tree-structured data-serialization language often used to create configuration files. | YAML Language | 11426805 | C190193 | 10/12/2022 |
| `ZIP` | An archive file format that supports lossless data compression. It is used to compress one or more files together into a single location. | ZIP Format | 11426806 | C190192 |  |

### **`size`**

**Formal Name: `caDSR CDE 11479876 v1.00`** ([Link](https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=11479876%20and%20ver_nr=1))

This metadata element is defined by the caDSR as "The measure (in bytes) of how much space a data file takes up on a storage medium.". No permissible values are defined for this CDE.

### **`checksums.md5`**

**Formal Name: `caDSR CDE 11556150 v1.00`** ([Link](https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=11556150%20and%20ver_nr=1))

This metadata element is defined by the caDSR as "A 32-character hexadecimal number that is computed on a file.". No permissible values are defined for this CDE.

### **`description`**

**Formal Name: `caDSR CDE 11280338 v1.00`** ([Link](https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=11280338%20and%20ver_nr=1))

This metadata element is defined by the caDSR as "A free text field that can be used to document the content and other details about an electronic file that may not be captured elsewhere.". No permissible values are defined for this CDE.