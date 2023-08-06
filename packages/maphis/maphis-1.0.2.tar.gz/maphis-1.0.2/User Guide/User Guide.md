# Arthropod Describer User Guide

## Outline

1) [Segmentation Hierarchy](#segmentation-hierarchy)
2) [Common Workflow](#common-workflow)
   1) [Creating a New Project](#1-creating-a-new-project)
   2) [Segmenting the Photos](#2-segmenting-the-photos)
   3) [Manually Adjusting the Segmentations](#3-manually-adjusting-the-segmentations)
   4) [Checking the Reflections](#4-checking-the-reflections)
   5) [Computing Measurements and Exporting the Results](#5-computing-measurements-and-exporting-the-results)

---

## Segmentation Hierarchy

The main task of the application is to segment photos of specimen (such as arthropods) into several regions (such as “head”, “thorax”, “left leg 1”, “femur of left leg 1”…), and then compute and export measurements describing those regions.

Each photo can be segmented at several hierarchical levels of “detail”. The `Body parts segmenter` plugin that is available by default generates segmentations with four levels:

1) The first level, called `Specimen`, simply divides the photo into `specimen` and `nothing` (or background):
![HierarchySpecimen.png](./Images/HierarchySpecimen.png)
&nbsp;  
2) The second level, called `Body/Legs`,  divides `specimen` into `body` and `legs`:
![HierarchyBodyLegs.png](./Images/HierarchyBodyLegs.png)
&nbsp;  
3) The third level, called `Segments`,  divides `body` into `head`, `thorax`, and `abdomen`,
&nbsp;  
and also `legs` into `leg1L`, `leg1R`, `leg2L`, `leg2R`, etc. (in this example, this also includes antennae):
![HierarchySegments.png](./Images/HierarchySegments.png)
&nbsp;  
4) The fourth level, called `Sections`,  divides individual `leg1L` etc. regions into `leg1LP1`, `leg1LP2`, and `leg1LP3`:
![HierarchySections.png](./Images/HierarchySections.png)

Different segmentation plugins (designed to segment other things than arthropods) may generate different hierarchies, with different names and numbers of regions or even hierarchy levels.

Measurements can be taken for any region at any level of the hierarchy.

---

## Common Workflow

### 1. Creating a New Project

**As the first stage of a normal workflow, you will need to create a project.**

1) Start the application.
&nbsp;  
&nbsp;  
2) Select `File/New project...` from the menu.
![NewProject.png](./Images/NewProject.png)
&nbsp;  
3) Type a name for the new project (e.g. “My1stProject”) in `Project name`, and choose the destination folder where the project should be saved (e.g. “D:\\work\\arthropods\\Projects”) in `Project folder destination`. All data for this project will then be saved under “D:\\work\\arthropods\\Projects\\My1stProject”.
![NewProjectName.png](./Images/NewProjectName.png)
&nbsp;  
4) To choose some starting photos to include in the project, click `Photo folder: Browse...`, go to the folder with your images and click `Select Folder`.
![NewProjectSelectFolder.png](./Images/NewProjectSelectFolder.png)
&nbsp;  
5) Thumbnails of the photos found in the selected folder will appear, and the automatic detection of the scale markers in the photos will begin. Wait until it finishes (it may take a while; the button at the bottom will be displaying the progress).
![NewProjectReadingScale.png](./Images/NewProjectReadingScale.png)
&nbsp;  
6) After the scale detection finishes and the countdown disappears, you will see the detected scale next to the thumbnails of photos for which it succeeded. If the scale detection failed for some photos, you will be able to set their scale manually. You can also rotate or downscale the photos before importing them into the project, if necessary.
![NewProjectCreate.png](./Images/NewProjectCreate.png)
&nbsp;  
7) When all photos have been prepared for import, click `Create`. The project will be created and you will see the main window: the list of all photos in this project on the left, the selected photo in the center, and the toolbox on the right:
![NewProjectJustCreated.png](./Images/NewProjectJustCreated.png)

---

##### Setting the scale manually, rotating and downscaling the images:

If the automatic scale detection failed for some photos, or you need to make some size and rotation adjustments after step 6) above, you can do so manually.

1) To adjust the scale and rotation of a photo, double-click the `Scale` cell of its table row to open a setting window.
![NewProjectSetScale.png](./Images/NewProjectSetScale.png)
&nbsp;  
2) You can zoom (by scrolling the mouse wheel) and pan around the photo (by holding the mouse wheel down and dragging). Find the scale marker, and draw a line along it by dragging with the left mouse button.
![NewProjectSetScaleLine.png](./Images/NewProjectSetScaleLine.png)
&nbsp;  
3) At the top of the window, specify what size the line should represent (e.g. “2 mm”) and click `Accept`.
![NewProjectSetScaleAccept.png](./Images/NewProjectSetScaleAccept.png)
&nbsp;  
4) You can also rotate the photo by clicking the buttons in the upper left corner. For most of the segmentation and other plugins to work properly, the specimen should be in the canonical orientation: head upwards.
&nbsp;  
&nbsp;  
5) To downscale a photo (e.g. to speed up processing), double-click the `New size (px)` cell of its table row, set the desired size and confirm with `OK`.
![NewProjectDownscale.png](./Images/NewProjectDownscale.png)

---

##### Adding More Photos to a Project:

At any later point, you can add more photos to the current project. To do this, use `File/Import photos...`. A window will appear, similar to the one you used to create a new project. Select a folder containing more photos, wait for the scale values to be determined, adjust them in case the automated detection failed anywhere, and click `Import`. 

---

### 2. Segmenting the Photos

**As the second stage of a normal workflow, you will want to segment the photos using one of the available segmentation plugins.**

1) At the top of the toolbox on the right side, select the plugin that should be used (e.g. `Body parts segmenter`).
![SegmentationSelectPlugin.png](./Images/SegmentationSelectPlugin.png)
&nbsp;  
2) If the plugin has any parameters that you can adjust, they will appear below the plugin selection.
&nbsp;  
&nbsp;  
3) After selecting the plugin and adjusting any parameters, click `Apply` (to segment the current photo) or `Apply to all` (to segment all photos in the project). Wait for the results to be computed.
&nbsp;  
    > NOTE: The application may appear to be not responding during this step. Please allow up to a minute for the segmentation to finish.

    ![SegmentationJustSegmented.png](./Images/SegmentationJustSegmented.png)
&nbsp;  
4) You will then see the photo segmented at the top level of the hierarchy (`Specimen`), into two classes labeled `specimen` and `nothing` (or background). To view the segmentation at a different hierarchy level, select a different label from the toolbox on the right (e.g. `thorax` to view the `Segments` hierarchy level):
![SegmentationThoraxSelected.png](./Images/SegmentationThoraxSelected.png)
&nbsp;  
You can adjust the segmentation display by modifying the opacity of the color overlay, or by switching between the `Filled` and `Outline` modes in the `Mask style` panel at the top.

---

### 3. Manually Adjusting the Segmentations

**As the third stage of a normal workflow, you will check if the automatic segmentation produced good results, and make manual adjustments if necessary.**

You will notice that the thumbnail of each photo in the list on the left shows several yellow dots in the corner. These represent individual levels of the segmentation hierarchy, and whether the segmentation at that level has been approved (a large green dot), or not (a small yellow dot).

The approvals do not influence any calculations, they only serve as a way for you to mark that you consider the segmentation good and finished. Usually, you will check the results of the automatic segmentation of each photo, make any necessary manual corrections, and then mark the approval for all levels of the segmentation hierarchy in the `Approved levels` panel above the photo.

If you don't finish touching up the whole segmentation hierarchy of a photo in one go, you can also approve only the higher levels, and leave the more detailed ones for later.

It is also possible to create a full segmentation hierarchy completely manually, without using any segmentation plugin first.

---

##### Region Labels:

The editing tools use a “current” or “active” region label — the equivalent of color in image editing software. To select a region label (e.g. `thorax`), simply click in the list on the right. The list contains all available region labels and shows where in the segmentation hierarchy they belong.

Be careful — some region labels may not be meant for direct use. For instance, it may be improper to draw a new area using the `body` label, because each pixel belonging to the specimen's body should actually belong to one of its subregions: `head`, `thorax`, or `abdomen` (the newly drawn area would belong to none of these). If possible, always use the most specific label when editing the segmentation.

---

##### Editing Tools:

There are several tools available for manual editing, which should be familiar from common image editing software. You can activate and deactivate the tools by clicking their buttons in the toolbox on the right. Individual editing actions can be undone with `Ctrl + Z` and redone with `Ctrl + Y`. You can also zoom (by scrolling the mouse wheel) and pan around the photo (by holding the mouse wheel down and dragging)

> NOTE: Currently, the application may be a bit unresponsive and experience a brief “stutter” after each drawing operation such as a brush stroke.

- `Brush` serves as the simplest editing tool. You can specify the brush radius, and then draw by dragging the mouse.

- `Bucket` flood-fills the clicked area with the currently selected label. Use this e.g. to quickly re-label or erase a region (when `nothing` is the active label).

- `Knife` lets you draw a straight-line cut across the segmentation by dragging the mouse. This can be used for splitting a region into subregions. The cut can be made using any label, or `nothing`.

- `Polygon` lets you specify a region by drawing its boundary. You can combine left-clicking to place individual vertices, and dragging the mouse with the button held to draw freehand sections. Double-click to finish the polygon.

- `Ruler` isn't used for editing, but for quick measurements. Simply drag a line over the photo to measure a distance. If `Multiple measurements` is checked, you can place multiple rulers over the photo. Right-click the mouse to remove all rulers.
![Ruler.png](./Images/Ruler.png)

---

##### Using Drawing Constraints:

To help you “stay between the lines” while drawing, you can use the constraint system. For instance, if you only want to change the way the specimen is segmented into individual parts, but are otherwise happy with the specimen's overall contour, you can limit all changes to within the current `specimen` boundaries.

As you move the mouse cursor over the list of available region labels on the right, you will see a `Set constraint` button available next to each region:
![ConstraintButton.png](./Images/ConstraintButton.png)

If you click this button, all further edits will be limited to that region, and no pixels outside it will be modified:
![ConstraintActivated.png](./Images/ConstraintActivated.png)

In this example, you can set the constraint to the `body` region while painting with the `head` label — this will allow you to easily turn a bit of mislabeled `thorax` into `head` with only a few quick, imprecise brush strokes, without fear of breaking the overall contour of `body`:
![ConstraintUsed.png](./Images/ConstraintUsed.png)

When you are done, you can re-enable editing the whole photo by clicking the `Remove constraint` button.

You can also hold down the `Ctrl` key and scroll the mouse wheel up or down to cycle between all constraints that are relevant for the currently selected label, at the current cursor location. For instance, if you have `leg1LP1` as the active label, and the mouse cursor is hovering over the middle section of the first left leg, the system will cycle between the following constraints: none, `specimen`, `legs`, `leg1L`, `leg1LP2`. 

---

### 4. Checking the Reflections

**After finalizing the segmentations, you may want to check the reflections in the photos.**

“Reflections” refer to the pixels where the color information in the photo is unreliable, because it is not showing the color of the specimen, but reflected light. Because of this, these areas should be excluded from computing any color- or texture-related properties.

1) To view the reflection areas automatically detected by the segmentation plugin, select `Reflections` in the `Active mask` panel at the top.
![Reflections.png](./Images/Reflections.png)
&nbsp;  
2) You can then adjust the reflection mask with the same tools you used for the segmentation. Editing will be automatically constrained to the specimen at the highest level of the segmentation hierarchy. 
&nbsp;  
    > NOTE: If the reflection mask is difficult to see (e.g. white on white), you can change the color of the mask by double-clicking the color square next to `Reflection` in the list of labels on the right, and picking a more contrasting color, like magenta. 
&nbsp;    
3) After you are content with the reflection mask, i.e. it covers all places where the color of the specimen is not shown accurately, you can mark it as approved at the top of the window (this doesn't influence anything and only serves as a note).

---

### 5. Computing Measurements and Exporting the Results

**As the final stage of a normal workflow, you will select which properties you want measured for which regions, and export the results to a spreadsheet. Generally, you will want to do this after all segmentations and reflections have been approved.**

1) Select the `Measurements` tab at the top of the window. A table for all computed measurements for all photos in the project — initially empty — will appear.
![MeasurementsEmpty.png](./Images/MeasurementsEmpty.png)
&nbsp;  
2) Click `Compute new measurements` to open a dialog in which you will select which measurements to compute for which regions.
&nbsp;  
&nbsp;  
3) The dialog consists of three panels: the list of all regions available in the photos, the list of all possible measurements, and then the list showing the combinations that you selected and want to compute. To fill the third list, make selections in the first two lists by clicking, and then press the `Assign` button in the middle. 
![MeasurementsSelect.png](./Images/MeasurementsSelect.png)
&nbsp;  
Not all measurements are useful for all regions. For instance, this is how the list on the right will look if you make these three selections and assignments:
   * `Area` + `Circularity` for `specimen`, `body`, `head`, `thorax`, `abdomen`
   * `GLCM Contrast` for `body`
   * `Geodesic length` + `Mean width` for `leg1L`, `leg1R`
   
    ![MeasurementsApply.png](./Images/MeasurementsApply.png)
&nbsp;  
4) Once you have specified which measurements you want to compute for which regions, click `Apply` and wait for the results to appear.
&nbsp;  
    > NOTE: The application may appear to be not responding during this step. Please allow some time for the computations to finish.

    ![MeasurementsExport.png](./Images/MeasurementsExport.png)
Values of simple measurements can be inspected directly in the table. More complex values like matrices for the GLCM properties can be inspected by double-clicking their cells.
&nbsp;  
&nbsp;
6) Finally, click the `Export to [XLSX]` button at the top to export the results as an Excel spreadsheet. Alternatively, you can click the little down arrow next to the button and choose CSV as the export format.
    > NOTE: If some more “verbose” measurements like the GLCM properties have been selected, the results may be stored on more than one sheet inside the XLSX file, or in more than one CSV file.

---

##### Available Measurements:

- **Basic properties:**
  - **Area**: The total area of the region.
  - **Mean intensity**: The mean R, G, B values in the region (excluding any pixels marked as reflections). 
  - **Circularity**: A value from 0.0 to 1.0, where 1.0 = perfect circle.
  - **Max Feret**: The maximum Feret diameter (caliper size) of the region.
  - **Geodesic length**: The maximum within-region length from one of its “ends” to the other. Useful for elongated regions like legs (measures along the bent leg, not in a straight line).
  - **Mean width**: Double of the mean distance to the region's boundary from its morphological skeleton. Useful for elongated regions like legs.
  - **Contour**: A vector of 40 half-widths of the region perpendicular to its main axis, spaced at regular intervals. Can be used to reconstruct, plot, and compare the basic “shape” of a region. Useful for the main specimen body.
&nbsp;  
&nbsp;  
- **GLCM properties**: These texture properties are derived from the grey-level co-occurrence matrices calculated separately for the H, S, V channels of the region (excluding any reflections). For each of the channels, the result is a 2D matrix `distances × angles` describing one of the relationships (list below) between pixels a certain distance apart, in a certain direction.
&nbsp;  
&nbsp;  
For instance, `ContrastV(0.1 mm, 90°)` describes how contrasting the pixels in the V channel (which corresponds to the brightness) that are 0.1 mm apart at an angle of 90° tend to be. These values can be used to characterize patterns such as vertical or horizontal stripes of certain sizes, etc.
&nbsp;  
&nbsp;  
  (For background and explanation of individual sub-properties, refer to
&nbsp;  
    > _Haralick, R. M.; Shanmugam, K.; Dinstein, I., “Textural features for image classification” IEEE Transactions on systems, man, and cybernetics 6 (1973): 610-621. [DOI:10.1109/TSMC.1973.4309314](https://doi.org/10.1109/TSMC.1973.4309314)_

  or to [https://scikit-image.org/docs/stable/api/skimage.feature.html#skimage.feature.graycoprops](https://scikit-image.org/docs/stable/api/skimage.feature.html#skimage.feature.graycoprops).)
  - **Contrast**
  - **Dissimilarity**
  - **Homogeneity**
  - **ASM**
  - **Energy**
  - **Correlation**
