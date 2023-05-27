function displayEntityTree(jsonResult){
    const rootEntityTree = extractEntityTreeRoot(jsonResult);
    const divID = "entityTree";
    cleanCanvas(divID);
    am5.ready(function() {

        const root = am5.Root.new(divID);
        root.setThemes([am5themes_Animated.new(root)]);
        
        const treeSettings = {
            container: am5.Container.new(root, {
                width: am5.percent(100),
                height: am5.percent(100),
                layout: root.verticalLayout
            }),
            type: am5hierarchy.Tree.new(root, {
                singleBranchOnly: false,
                downDepth: 1,
                initialDepth: 10,
                valueField: "depth",
                categoryField: "name",
                childDataField: "children",
                centerStrength: 0.5
            }),
            links:{
                strokeWidth: 3,
                strokeOpacity: 0.5,
                templateField: "linkSettings",
            },
            nodes:{
                radius: 22,
                templateField: "circleSettings"
            }
        }

        const container = root
            .container
            .children
            .push(treeSettings.container);

        const series = container
            .children
            .push(treeSettings.type);
        series
            .links
            .template
            .setAll(treeSettings.links);      
        series
            .circles
            .template
            .setAll(treeSettings.nodes);
        series
            .data
            .setAll([rootEntityTree]);
        series
            .set("selectedDataItem", series.dataItems[0]);
        series
            .appear(1000, 100);

    }); 
}