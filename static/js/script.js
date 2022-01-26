$(function () {
    //burgerbtn
    $(function(){
        $('.burger_btn').on('click',function(){
            $('.burger_btn').toggleClass('close');
            $('.header_modal').slideToggle(500);
        });
    });

    //checkbox
    
    $(function() {
    let check_list = ".check_list";//検索範囲
    let list_item = ".article_items";//検索対象
    let hideItem = "hide_item";//付与クラス

    //絞り込み条件の変更
    $(function() {
        $(document).on("change", check_list + " input", function() {
            search_filter();
        });
    });

    function search_filter() {
        $(list_item).removeClass(hideItem);
        for (let i = 0; i < $(check_list).length; i++) {
            let name = $(check_list).eq(i).find("input").attr("name");
            let searchData = get_selected_input_items(name);
            console.log(searchData);
            if (searchData.length === 0 || searchData[0] === "") {
                continue;
            }
            for (let j = 0; j < $(list_item).length; j++) {
                let itemData = get_setting_values_in_item($(list_item).eq(j), name);
                console.log(itemData);
                let check = array_match_check(itemData, searchData);
                if (!check) {
                    $(list_item).eq(j).addClass(hideItem);
                }
            }
        }
    }

    //チェックの入った値の取得
    function get_selected_input_items(name) {
        let searchData = [];
        $("[name="+name+"]:checked").each(function() {
            searchData.push($(this).val());
        });
        return searchData;
    }

    //対象の一覧を取得
    function get_setting_values_in_item(target, data) {
        let itemData = target.data(data);
        if (!Array.isArray(itemData)) {
            itemData = [itemData];
        }
        return itemData;
    }

    //対象との比較
    function array_match_check(arr1,arr2) {
        let arrCheck = false;
        for (let i = 0; i < arr1.length; i++) {
            if (arr2.indexOf(arr1[i]) >= 0) {
                arrCheck = true;
                break;
            }
        }
        return arrCheck;
    }
    });

    //destroy_judge
    $(function(){
        $('.destroy_icon').on('click',function(){
            $('.judge_modal').fadeIn(300);
        });
    });
    $(function(){
        $('.close_modal').on('click',function(){
            $('.judge_modal').fadeOut(300);
        });
    });
})