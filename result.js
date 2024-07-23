const { Builder, By, until } = require('selenium-webdriver');
const fs = require('fs');
const { parse } = require('json2csv');

async function scrape(reg) {
    let retry = 3;
    let data = { "REGISTER": reg, "NAME": null, "CGPA": null };
    
    while (retry > 0) {
        let driver = await new Builder().forBrowser('chrome').build();
        try {
            await driver.get('http://www.srkrexams.in/Login.aspx');

            let user_xpath = "/html/body/form/div[4]/div/div/div[2]/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div/input";
            let user_keys = await driver.findElement(By.xpath(user_xpath));
            await user_keys.sendKeys(reg);

            let password_xpath = "/html/body/form/div[4]/div/div/div[2]/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div/input";
            let pass_key = await driver.findElement(By.xpath(password_xpath));
            await pass_key.sendKeys(reg);

            let login_xpath = "/html/body/form/div[4]/div/div/div[2]/div[3]/div/div/div[2]/div[1]/div/div[2]/div/div[3]/div/input";
            let login_click = await driver.findElement(By.xpath(login_xpath));
            await login_click.click();

            await driver.wait(until.elementLocated(By.xpath("/html/body/form/div[5]/div[3]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div[1]/div[2]/div/div/table/tbody/tr[7]/td[3]/span")), 3000);
            let cgpa_xpath = "/html/body/form/div[5]/div[3]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div[1]/div[2]/div/div/table/tbody/tr[7]/td[3]/span";
            let cgpa = await driver.findElement(By.xpath(cgpa_xpath));
            data['CGPA'] = await cgpa.getText();

            let name_xpath = "/html/body/form/div[5]/div[3]/div/div/div/div[1]/div/div/div/div/div/div[1]/div/div[2]/label";
            let name = await driver.findElement(By.xpath(name_xpath));
            data['NAME'] = await name.getText();

            break;

        } catch (error) {
            console.log(`No such element found for ${reg}. Retrying...`);
            retry -= 1;
        } finally {
            await driver.quit();
        }
    }
    return data;
}

function generateCodes() {
    let codes = [];
    let prefix = "21B91A12";
    for (let i = 90; i < 100; i++) {
        if (i < 10) {
            codes.push(prefix + "0" + i);
        } else {
            codes.push(prefix + i);
        }
    }
    return codes;
}

(async function main() {
    let regids = generateCodes();
    let results = [];
    for (let i of regids) {
        let result = await scrape(i);
        results.push(result);
    }
    const csv = parse(results);
    fs.writeFileSync('it.csv', csv);
})();

