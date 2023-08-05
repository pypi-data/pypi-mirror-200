==============
Run CamoTSS
==============

CamoTSS includes two kind of modes : TC mode and CTSS mode. 

The input files include:

* alignment file (bam file)
* annotation file (gtf file)
* cell list file and reference genome file (fasta file)
* cell barcode list file (csv file)

The output files include:

* cell by all TSSs matrix (h5ad)
* cell by two TSSs matrix (h5ad) 
* cell by CTSS matrix (h5ad)
* cell by CTSS matrix (h5ad) 

Here are test file in the directory : **test**.  



Filtering UMI according to the specific criteria:

.. code-block:: html

* Have a MAPQ score of 255
* Maps to exactly one gene
* Overlaps an exon by at least 50% in a way consistent with annotated splice junctions and strand annotation. Records that align to exons will have an RE:A:E tag.
* Remove any records with matching UMI and Barcode values that map to different genes.


For more information, you can check this material_ .

.. _material: https://www.10xgenomics.com/resources/analysis-guides/tutorial-navigating-10x-barcoded-bam-files

To get cleaner bam, you can process possorted_genome_bam.bam according to the following steps.

.. code-block:: linux

   1. cd /cellranger_out/outs
   2. samtools view  possorted_genome_bam.bam | LC_ALL=C grep "xf:i:25" > body_filtered_sam
   3. samtools view -H possorted_genome_bam.bam > header_filted_sam
   4. cat header_filted_sam body_filtered_sam > possorted_genome_bam_filterd.sam
   5. samtools view -b possorted_genome_bam_filterd.sam > possorted_genome_bam_filterd.bam
   6. samtools index possorted_genome_bam_filterd.bam possorted_genome_bam_filterd.bam.bai

In most instances, we want to detect alternative TSS usage among various samples.
We should run CamoTSS at the same batch for all of these samples.
To accomplish this goal, it is necessary to merge bam file of these samples to one bam file.
We should add suffix to cell barcode of each sample in order to distinguish origin of samples.
The following script can help you manually add sample information to cell barcode.


