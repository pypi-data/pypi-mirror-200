import { ref } from 'vue'

export default {
    props: {},
    setup(props) {

        const msg = ref('hello')

        return {
            msg
        };
    },
    components: {  }
}