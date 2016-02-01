import Debug from "debug";
import { range } from "lodash/util";
import { random } from "lodash/number";

const debug = Debug("examist:api");

export default class API {
    constructor(key) {
        this.key = key;
    }

    static request(method, url, data = {}, headers = {}) {
        debug(`>> %c${method.toUpperCase()} ${url}${headers["Auth-Key"] ? " (authorized)" : ""}`, "color: purple", data);

        return new Promise((resolve) => {
            setTimeout(resolve.bind(this, {
                req: { code: 200 },
                body: "Success"
            }), 300);
        });
    }

    request(method, url, data) {
        return API.request(method, url, data, { "Auth-Key": this.key });
    }

    /**
     * Log the user into the API.
     * @param  {Object} details { username, password }
     * @return {Promise} -> {Object}
     */
    static login({ username, password }) {
        return API.request("POST", "/login", { username, password }).then(() => ({
            id: 1,
            username: "adrian",
            name: "Adrian Cooney",
            email: "cooney.adrian@gmail.com",
            loading: false,
            key: "f89sf0n7f0as97fn90sa7fn" 
        }));
    }

    static signup({ username, email, password }) {
        return API.request("POST", "/login", { username, email, password });
    }

    /**
     * Get university by their domain name. e.g. nuigalway.ie. Used when
     * finding the university on the signup page.
     * @param  {String} domain The university domain.
     * @return {Promise} -> {Insititution}
     */
    static getInstitutionByDomain(domain) {
        return API.request("GET", `/institution/search?q=${domain}`).then(() => ({
            id: 1,
            shorthand: "NUIG",
            name: "National University of Ireland, Galway",
            image: "http://www.nuigalway.ie/cdn/images/dropdown-thumb-1.jpg",
            domain: "nuigalway.ie",
            colors: {
                primary: "#68085B",
                secondary: "#7DB8C5"
            },
            stats: {
                students: 312,
                modules: 1249,
                papers: 14940
            }
        }));
    }

    /**
     * Get the current logged in user's own modules.
     * @return {Promise} -> {Object{modules: Array}}
     */
    getModules() {
        return this.request("GET", "/profile/modules").then(() => ({
            modules: range(6).map(() => {
                return {
                    code: "CT" + Math.floor(Math.random() * 1000)
                }
            })
        }))
    }

    /**
     * Get a module by code.
     * @param  {String} code Code e.g. CT470
     * @return {Promise} -> {Object}
     */
    getModule(code) {
        return this.request("GET", `/module/${code}`).then(() => ({
            module: Generator.module(code)
        }));
    }

    /**
     * Get a paper module, year, period.
     * @param  {String} module Code e.g. CT470
     * @param  {Number} year   The year e.g. 2007
     * @param  {String} period One of ["summer", "winter", "autumn", "spring"]
     * @return {Promise} -> {Object}
     */
    getPaper(module, year, period) {
        return this.request("GET", `/module/${module}/paper/${year}/${period}`).then(() => ({
            paper: Generator.paper(module, year, period)
        }));
    }
}

/*
 * Dummy data generators
 */
const Generator = {
    module(code) {
        return {
            code,
            name: "Maths",
            papers: range(5).map((v, i) => ({ 
                ...Generator.paper(code, 2015 - i, ["autumn", "winter", "summer"][random(0, 2)]),
                isIndexed: random(0, 1) == 0
            }))
        }
    },

    paper(module, year, period) {
        let id = Generator.getUID();
        return {
            id,
            questions: range(10).map(Generator.question.bind(null, id)),
            module, year, period
        };
    },

    question(paper) {
        return {
            paper,
            id: Generator.getUID(),
            content: "What is the highest point on planet earth?",
            path: [1, 1]
        }
    },

    __uid: 0,
    getUID() {
        return Generator.__uid++;
    }
};